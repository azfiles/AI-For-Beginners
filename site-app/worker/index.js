const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "private, no-store",
  "x-content-type-options": "nosniff",
};

const MAX_BODY_BYTES = 900_000;
const MAX_NOTES = 500;
const MAX_PROGRESS = 200;

const NOTE_UPSERT = `
  INSERT INTO learning_notes (
    user_id, id, path, page_title, source, quote, note_text,
    block_index, anchor, created_at, updated_at
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
  ON CONFLICT(user_id, id) DO UPDATE SET
    path = excluded.path,
    page_title = excluded.page_title,
    source = excluded.source,
    quote = excluded.quote,
    note_text = excluded.note_text,
    block_index = excluded.block_index,
    anchor = excluded.anchor,
    updated_at = CURRENT_TIMESTAMP
`;

const PROGRESS_UPSERT = `
  INSERT INTO learning_progress (
    user_id, path, title, source, completed_at, updated_at
  ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
  ON CONFLICT(user_id, path) DO UPDATE SET
    title = excluded.title,
    source = excluded.source,
    completed_at = excluded.completed_at,
    updated_at = CURRENT_TIMESTAMP
`;

function json(value, status = 200) {
  return new Response(JSON.stringify(value), { status, headers: JSON_HEADERS });
}

function getUser(request) {
  const userId = request.headers.get("oai-authenticated-user-id")?.trim();
  if (!userId) return null;
  return {
    id: userId,
    email: request.headers.get("oai-authenticated-user-email")?.trim() || null,
  };
}

function sameOrigin(request) {
  const url = new URL(request.url);
  const origin = request.headers.get("origin");
  if (origin && origin !== url.origin) return false;
  const fetchSite = request.headers.get("sec-fetch-site");
  return !fetchSite || ["same-origin", "same-site", "none"].includes(fetchSite);
}

function text(value, max, fallback = "") {
  return typeof value === "string" ? value.slice(0, max) : fallback;
}

function path(value) {
  if (typeof value !== "string" || !value.startsWith("/") || value.startsWith("//")) return "/";
  return value.slice(0, 1500);
}

function timestamp(value) {
  if (typeof value !== "string" || value.length > 40 || Number.isNaN(Date.parse(value))) {
    return new Date().toISOString();
  }
  return new Date(value).toISOString();
}

function identifier(value) {
  return typeof value === "string" && /^[A-Za-z0-9_-]{1,128}$/.test(value) ? value : null;
}

function normalizeNote(value) {
  if (!value || typeof value !== "object") return null;
  const id = identifier(value.id);
  const quote = text(value.quote, 1200).trim();
  if (!id || !quote) return null;
  return {
    id,
    path: path(value.path),
    pageTitle: text(value.pageTitle, 300, "课程页面"),
    source: text(value.source, 1000),
    quote,
    text: text(value.text, 4000),
    blockIndex: Number.isInteger(value.blockIndex) ? Math.max(-1, Math.min(value.blockIndex, 10000)) : -1,
    anchor: text(value.anchor, 300),
    createdAt: timestamp(value.createdAt),
  };
}

function normalizeProgress(value) {
  if (!value || typeof value !== "object") return null;
  return {
    path: path(value.path),
    title: text(value.title, 300, "课程页面"),
    source: text(value.source, 1000),
    completedAt: timestamp(value.completedAt),
  };
}

async function readBody(request) {
  const declared = Number(request.headers.get("content-length") || 0);
  if (declared > MAX_BODY_BYTES) throw new RangeError("request too large");
  const raw = await request.text();
  if (raw.length > MAX_BODY_BYTES) throw new RangeError("request too large");
  return JSON.parse(raw || "{}");
}

async function readState(db, userId) {
  const [notesResult, progressResult] = await db.batch([
    db.prepare(`
      SELECT id, path, page_title, source, quote, note_text, block_index,
             anchor, created_at
      FROM learning_notes
      WHERE user_id = ?
      ORDER BY created_at DESC, id DESC
      LIMIT ?
    `).bind(userId, MAX_NOTES),
    db.prepare(`
      SELECT path, title, source, completed_at
      FROM learning_progress
      WHERE user_id = ?
      ORDER BY completed_at DESC, path ASC
      LIMIT ?
    `).bind(userId, MAX_PROGRESS),
  ]);

  const notes = (notesResult.results || []).map((row) => ({
    id: row.id,
    path: row.path,
    pageTitle: row.page_title,
    source: row.source,
    quote: row.quote,
    text: row.note_text,
    blockIndex: row.block_index,
    anchor: row.anchor,
    createdAt: row.created_at,
  }));
  const completed = {};
  for (const row of progressResult.results || []) {
    completed[row.path] = {
      path: row.path,
      title: row.title,
      source: row.source,
      completedAt: row.completed_at,
    };
  }
  return { version: 2, notes, completed };
}

function noteStatement(db, userId, note) {
  return db.prepare(NOTE_UPSERT).bind(
    userId,
    note.id,
    note.path,
    note.pageTitle,
    note.source,
    note.quote,
    note.text,
    note.blockIndex,
    note.anchor,
    note.createdAt,
  );
}

function progressStatement(db, userId, entry) {
  return db.prepare(PROGRESS_UPSERT).bind(
    userId,
    entry.path,
    entry.title,
    entry.source,
    entry.completedAt,
  );
}

async function handleLearning(request, env) {
  const user = getUser(request);
  if (!user) return json({ error: "authentication_required" }, 401);
  if (!env.DB) return json({ error: "database_unavailable" }, 503);

  if (request.method === "GET") {
    try {
      return json({ ...(await readState(env.DB, user.id)), account: { email: user.email } });
    } catch (error) {
      console.error("learning state read failed", error);
      return json({ error: "learning_state_unavailable" }, 503);
    }
  }

  if (request.method !== "POST") {
    return new Response(null, { status: 405, headers: { allow: "GET, POST" } });
  }
  if (!sameOrigin(request)) return json({ error: "cross_origin_write_blocked" }, 403);

  let payload;
  try {
    payload = await readBody(request);
  } catch (error) {
    return json({ error: error instanceof RangeError ? "request_too_large" : "invalid_json" }, 400);
  }

  try {
    switch (payload.action) {
      case "upsert_note": {
        const note = normalizeNote(payload.note);
        if (!note) return json({ error: "invalid_note" }, 400);
        await noteStatement(env.DB, user.id, note).run();
        return json({ ok: true, note });
      }
      case "delete_note": {
        const id = identifier(payload.id);
        if (!id) return json({ error: "invalid_note_id" }, 400);
        await env.DB.prepare("DELETE FROM learning_notes WHERE user_id = ? AND id = ?").bind(user.id, id).run();
        return json({ ok: true });
      }
      case "set_progress": {
        const entry = normalizeProgress(payload.entry);
        if (!entry) return json({ error: "invalid_progress" }, 400);
        if (payload.completed) await progressStatement(env.DB, user.id, entry).run();
        else await env.DB.prepare("DELETE FROM learning_progress WHERE user_id = ? AND path = ?").bind(user.id, entry.path).run();
        return json({ ok: true });
      }
      case "merge": {
        const notes = Array.isArray(payload.notes)
          ? payload.notes.slice(0, MAX_NOTES).map(normalizeNote).filter(Boolean)
          : [];
        const progressInput = payload.completed && typeof payload.completed === "object" && !Array.isArray(payload.completed)
          ? Object.values(payload.completed).slice(0, MAX_PROGRESS)
          : [];
        const progress = progressInput.map(normalizeProgress).filter(Boolean);
        const statements = [
          ...notes.map((note) => noteStatement(env.DB, user.id, note)),
          ...progress.map((entry) => progressStatement(env.DB, user.id, entry)),
        ];
        if (statements.length) await env.DB.batch(statements);
        return json({ ok: true, imported: { notes: notes.length, progress: progress.length } });
      }
      default:
        return json({ error: "unsupported_action" }, 400);
    }
  } catch (error) {
    console.error("learning state write failed", error);
    return json({ error: "learning_state_write_failed" }, 503);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/learning") return handleLearning(request, env);
    if (!env.ASSETS?.fetch) return new Response("Static assets unavailable", { status: 503 });
    return env.ASSETS.fetch(request);
  },
};

export const __test = {
  getUser,
  sameOrigin,
  normalizeNote,
  normalizeProgress,
  handleLearning,
};
