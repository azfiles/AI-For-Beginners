import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { DatabaseSync } from "node:sqlite";

test("learning migration creates indexed user-owned tables", async () => {
  const db = new DatabaseSync(":memory:");
  const migration = await readFile(new URL("../drizzle/0000_fearless_stone_men.sql", import.meta.url), "utf8");
  for (const statement of migration.split("--> statement-breakpoint").map((value) => value.trim()).filter(Boolean)) {
    db.exec(statement);
  }

  const tables = db.prepare("SELECT name FROM sqlite_schema WHERE type = 'table' ORDER BY name").all().map((row) => row.name);
  assert.deepEqual(tables, ["learning_notes", "learning_progress"]);

  const indexes = db.prepare("SELECT name FROM sqlite_schema WHERE type = 'index' AND name NOT LIKE 'sqlite_%' ORDER BY name").all().map((row) => row.name);
  assert.deepEqual(indexes, ["idx_learning_notes_user_created", "idx_learning_progress_user_completed"]);

  const notePlan = db.prepare("EXPLAIN QUERY PLAN SELECT * FROM learning_notes WHERE user_id = ? ORDER BY created_at DESC").all("user-a");
  const progressPlan = db.prepare("EXPLAIN QUERY PLAN SELECT * FROM learning_progress WHERE user_id = ? ORDER BY completed_at DESC").all("user-a");
  assert.match(notePlan.map((row) => row.detail).join(" "), /idx_learning_notes_user_created/);
  assert.match(progressPlan.map((row) => row.detail).join(" "), /idx_learning_progress_user_completed/);

  db.close();
});
