CREATE TABLE `learning_notes` (
	`user_id` text NOT NULL,
	`id` text NOT NULL,
	`path` text NOT NULL,
	`page_title` text NOT NULL,
	`source` text DEFAULT '' NOT NULL,
	`quote` text NOT NULL,
	`note_text` text DEFAULT '' NOT NULL,
	`block_index` integer DEFAULT -1 NOT NULL,
	`anchor` text DEFAULT '' NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY(`user_id`, `id`)
);
--> statement-breakpoint
CREATE INDEX `idx_learning_notes_user_created` ON `learning_notes` (`user_id`,`created_at`);--> statement-breakpoint
CREATE TABLE `learning_progress` (
	`user_id` text NOT NULL,
	`path` text NOT NULL,
	`title` text NOT NULL,
	`source` text DEFAULT '' NOT NULL,
	`completed_at` text NOT NULL,
	`updated_at` text DEFAULT CURRENT_TIMESTAMP NOT NULL,
	PRIMARY KEY(`user_id`, `path`)
);
--> statement-breakpoint
CREATE INDEX `idx_learning_progress_user_completed` ON `learning_progress` (`user_id`,`completed_at`);--> statement-breakpoint
PRAGMA optimize;
