import assert from "node:assert/strict";
import test from "node:test";
import worker, { __test } from "../worker/index.js";

class FakeStatement {
  constructor(db, query) {
    this.db = db;
    this.query = query.replace(/\s+/g, " ").trim();
    this.values = [];
  }

  bind(...values) {
    this.values = values;
    return this;
  }

  async execute() {
    const q = this.query;
    if (q.startsWith("SELECT") && q.includes("FROM learning_notes")) {
      const [userId, limit] = this.values;
      const results = [...this.db.notes.values()].filter((row) => row.user_id === userId).slice(0, limit);
      return { results };
    }
    if (q.startsWith("SELECT") && q.includes("FROM learning_progress")) {
      const [userId, limit] = this.values;
      const results = [...this.db.progress.values()].filter((row) => row.user_id === userId).slice(0, limit);
      return { results };
    }
    if (q.startsWith("INSERT INTO learning_notes")) {
      const [user_id, id, path, page_title, source, quote, note_text, block_index, anchor, created_at] = this.values;
      this.db.notes.set(`${user_id}:${id}`, { user_id, id, path, page_title, source, quote, note_text, block_index, anchor, created_at });
      return { success: true };
    }
    if (q.startsWith("INSERT INTO learning_progress")) {
      const [user_id, path, title, source, completed_at] = this.values;
      this.db.progress.set(`${user_id}:${path}`, { user_id, path, title, source, completed_at });
      return { success: true };
    }
    if (q.startsWith("DELETE FROM learning_notes")) {
      this.db.notes.delete(`${this.values[0]}:${this.values[1]}`);
      return { success: true };
    }
    if (q.startsWith("DELETE FROM learning_progress")) {
      this.db.progress.delete(`${this.values[0]}:${this.values[1]}`);
      return { success: true };
    }
    throw new Error(`Unhandled query: ${q}`);
  }

  all() { return this.execute(); }
  run() { return this.execute(); }
}

class FakeDB {
  constructor() {
    this.notes = new Map();
    this.progress = new Map();
  }
  prepare(query) { return new FakeStatement(this, query); }
  batch(statements) { return Promise.all(statements.map((statement) => statement.execute())); }
}

const authHeaders = (user, extra = {}) => ({
  "oai-authenticated-user-id": user,
  "oai-authenticated-user-email": `${user}@example.test`,
  ...extra,
});

test("normalizers enforce safe paths and bounded fields", () => {
  const note = __test.normalizeNote({
    id: "note_1",
    path: "https://evil.example/",
    quote: "q".repeat(1300),
    text: "t".repeat(5000),
    createdAt: "invalid",
  });
  assert.equal(note.path, "/");
  assert.equal(note.quote.length, 1200);
  assert.equal(note.text.length, 4000);
  assert.match(note.createdAt, /^\d{4}-\d{2}-\d{2}T/);
  assert.equal(__test.normalizeNote({ id: "bad id", quote: "x" }), null);
});

test("API rejects unauthenticated and cross-origin writes", async () => {
  const env = { DB: new FakeDB() };
  const anonymous = await __test.handleLearning(new Request("https://site.test/api/learning"), env);
  assert.equal(anonymous.status, 401);

  const crossOrigin = await __test.handleLearning(new Request("https://site.test/api/learning", {
    method: "POST",
    headers: authHeaders("user-a", { origin: "https://evil.example", "content-type": "application/json" }),
    body: JSON.stringify({ action: "merge", notes: [], completed: {} }),
  }), env);
  assert.equal(crossOrigin.status, 403);
});

test("notes and progress are isolated by authenticated user", async () => {
  const env = { DB: new FakeDB() };
  const note = {
    id: "note-a",
    path: "/lesson-a",
    pageTitle: "课程 A",
    source: "lesson-a.md",
    quote: "重点内容",
    text: "我的理解",
    blockIndex: 2,
    anchor: "part-a",
    createdAt: "2026-09-17T00:00:00.000Z",
  };
  const progress = { path: "/lesson-a", title: "课程 A", source: "lesson-a.md", completedAt: "2026-09-17T01:00:00.000Z" };

  for (const payload of [
    { action: "upsert_note", note },
    { action: "set_progress", completed: true, entry: progress },
  ]) {
    const response = await __test.handleLearning(new Request("https://site.test/api/learning", {
      method: "POST",
      headers: authHeaders("user-a", { origin: "https://site.test", "content-type": "application/json" }),
      body: JSON.stringify(payload),
    }), env);
    assert.equal(response.status, 200);
  }

  const userA = await (await __test.handleLearning(new Request("https://site.test/api/learning", { headers: authHeaders("user-a") }), env)).json();
  const userB = await (await __test.handleLearning(new Request("https://site.test/api/learning", { headers: authHeaders("user-b") }), env)).json();
  assert.equal(userA.notes.length, 1);
  assert.equal(Object.keys(userA.completed).length, 1);
  assert.equal(userB.notes.length, 0);
  assert.equal(Object.keys(userB.completed).length, 0);
});

test("non-API requests are delegated to the static asset binding", async () => {
  const env = { ASSETS: { fetch: async (request) => new Response(`asset:${new URL(request.url).pathname}`) } };
  const response = await worker.fetch(new Request("https://site.test/pages/example.html"), env);
  assert.equal(await response.text(), "asset:/pages/example.html");
});
