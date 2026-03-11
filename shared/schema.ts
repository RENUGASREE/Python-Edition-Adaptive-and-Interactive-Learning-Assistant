import { pgTable, text, serial, integer, boolean, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

export * from "./models/auth";
export * from "./models/chat";

// Content Structure
export const modules = pgTable("modules", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  description: text("description").notNull(),
  order: integer("order").notNull(),
  imageUrl: text("image_url"), // For dashboard cards
});

export const lessons = pgTable("lessons", {
  id: serial("id").primaryKey(),
  moduleId: integer("module_id").notNull(),
  title: text("title").notNull(),
  slug: text("slug").notNull(),
  content: text("content").notNull(), // Markdown content
  order: integer("order").notNull(),
  difficulty: text("difficulty").default("beginner"), // beginner, intermediate, advanced
  duration: integer("duration").notNull(), // Minutes to complete
});

export const quizzes = pgTable("quizzes", {
  id: serial("id").primaryKey(),
  lessonId: integer("lesson_id").notNull(),
  title: text("title").notNull(),
});

export const questions = pgTable("questions", {
  id: serial("id").primaryKey(),
  quizId: integer("quiz_id").notNull(),
  text: text("text").notNull(),
  type: text("type").default("multiple_choice"), // multiple_choice
  options: jsonb("options").notNull(), // Array of { text: string, correct: boolean }
  points: integer("points").default(10),
});

export const challenges = pgTable("challenges", {
  id: serial("id").primaryKey(),
  lessonId: integer("lesson_id").notNull(),
  title: text("title").notNull(),
  description: text("description").notNull(), // Markdown instructions
  initialCode: text("initial_code").notNull(),
  solutionCode: text("solution_code"), // Hidden from user
  testCases: jsonb("test_cases").notNull(), // Array of { input: string, expected: string }
  points: integer("points").default(20),
});

// User Progress
export const userProgress = pgTable("user_progress", {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(), // Matches auth.users.id
  lessonId: integer("lesson_id").notNull(),
  completed: boolean("completed").default(false),
  score: integer("score").default(0), // For quizzes
  lastCode: text("last_code"), // Saved code state
  completedAt: timestamp("completed_at"),
});

// Relations
export const modulesRelations = relations(modules, ({ many }) => ({
  lessons: many(lessons),
}));

export const lessonsRelations = relations(lessons, ({ one, many }) => ({
  module: one(modules, {
    fields: [lessons.moduleId],
    references: [modules.id],
  }),
  quizzes: many(quizzes),
  challenges: many(challenges),
  progress: many(userProgress),
}));

export const quizzesRelations = relations(quizzes, ({ one, many }) => ({
  lesson: one(lessons, {
    fields: [quizzes.lessonId],
    references: [lessons.id],
  }),
  questions: many(questions),
}));

export const questionsRelations = relations(questions, ({ one }) => ({
  quiz: one(quizzes, {
    fields: [questions.quizId],
    references: [quizzes.id],
  }),
}));

export const challengesRelations = relations(challenges, ({ one }) => ({
  lesson: one(lessons, {
    fields: [challenges.lessonId],
    references: [lessons.id],
  }),
}));

export const userProgressRelations = relations(userProgress, ({ one }) => ({
  lesson: one(lessons, {
    fields: [userProgress.lessonId],
    references: [lessons.id],
  }),
}));

// Schemas
export const insertModuleSchema = createInsertSchema(modules);
export const insertLessonSchema = createInsertSchema(lessons);
export const insertQuizSchema = createInsertSchema(quizzes);
export const insertQuestionSchema = createInsertSchema(questions);
export const insertChallengeSchema = createInsertSchema(challenges);
export const insertUserProgressSchema = createInsertSchema(userProgress);

// Types
export type Module = typeof modules.$inferSelect;
export type Lesson = typeof lessons.$inferSelect;
export type Quiz = typeof quizzes.$inferSelect;
export type Question = typeof questions.$inferSelect;
export type Challenge = typeof challenges.$inferSelect;
export type UserProgress = typeof userProgress.$inferSelect;

// API Types
export interface RunCodeRequest {
  code: string;
}

export interface RunCodeResponse {
  output: string;
  error?: string;
  passed: boolean;
}
