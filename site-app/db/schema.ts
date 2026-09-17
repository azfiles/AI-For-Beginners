import { sql } from "drizzle-orm";
import { index, integer, primaryKey, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const learningNotes = sqliteTable("learning_notes", {
  userId: text("user_id").notNull(),
  id: text("id").notNull(),
  path: text("path").notNull(),
  pageTitle: text("page_title").notNull(),
  source: text("source").notNull().default(""),
  quote: text("quote").notNull(),
  noteText: text("note_text").notNull().default(""),
  blockIndex: integer("block_index").notNull().default(-1),
  anchor: text("anchor").notNull().default(""),
  createdAt: text("created_at").notNull(),
  updatedAt: text("updated_at").notNull().default(sql`CURRENT_TIMESTAMP`),
}, (table) => [
  primaryKey({ columns: [table.userId, table.id] }),
  index("idx_learning_notes_user_created").on(table.userId, table.createdAt),
]);

export const learningProgress = sqliteTable("learning_progress", {
  userId: text("user_id").notNull(),
  path: text("path").notNull(),
  title: text("title").notNull(),
  source: text("source").notNull().default(""),
  completedAt: text("completed_at").notNull(),
  updatedAt: text("updated_at").notNull().default(sql`CURRENT_TIMESTAMP`),
}, (table) => [
  primaryKey({ columns: [table.userId, table.path] }),
  index("idx_learning_progress_user_completed").on(table.userId, table.completedAt),
]);
