import { db } from "./db";
import { 
  modules, lessons, quizzes, questions, challenges, userProgress,
  type Module, type Lesson, type Quiz, type Question, type Challenge, type UserProgress,
  insertUserProgressSchema
} from "@shared/schema";
import { eq, and, desc, asc } from "drizzle-orm";

export interface IStorage {
  // LMS
  getModules(): Promise<Module[]>;
  getModule(id: number): Promise<Module | undefined>;
  getLesson(id: number): Promise<Lesson | undefined>;
  getLessonWithDetails(id: number): Promise<Lesson & { module: Module, quizzes: (Quiz & { questions: Question[] })[], challenges: Challenge[] } | undefined>;
  
  // Progress
  getUserProgress(userId: string): Promise<UserProgress[]>;
  updateUserProgress(userId: string, progress: typeof userProgress.$inferInsert): Promise<UserProgress>;
}

export class DatabaseStorage implements IStorage {
  async getModules(): Promise<(Module & { lessons: Lesson[] })[]> {
    const allModules = await db.select().from(modules).orderBy(asc(modules.order));
    const modulesWithLessons = await Promise.all(
      allModules.map(async (module) => {
        const moduleLessons = await db
          .select()
          .from(lessons)
          .where(eq(lessons.moduleId, module.id))
          .orderBy(asc(lessons.order));
        return { ...module, lessons: moduleLessons };
      })
    );
    return modulesWithLessons;
  }

  async getModule(id: number): Promise<Module | undefined> {
    const [module] = await db.select().from(modules).where(eq(modules.id, id));
    return module;
  }

  async getLesson(id: number): Promise<Lesson | undefined> {
    const [lesson] = await db.select().from(lessons).where(eq(lessons.id, id));
    return lesson;
  }

  async getLessonWithDetails(id: number) {
    // This could be optimized with relations query
    const lesson = await this.getLesson(id);
    if (!lesson) return undefined;

    const module = await this.getModule(lesson.moduleId);
    if (!module) return undefined; // Should not happen

    const lessonQuizzes = await db.select().from(quizzes).where(eq(quizzes.lessonId, id));
    const quizzesWithQuestions = await Promise.all(lessonQuizzes.map(async (q) => {
      const qs = await db.select().from(questions).where(eq(questions.quizId, q.id));
      return { ...q, questions: qs };
    }));

    const lessonChallenges = await db.select().from(challenges).where(eq(challenges.lessonId, id));

    return {
      ...lesson,
      module,
      quizzes: quizzesWithQuestions,
      challenges: lessonChallenges,
    };
  }

  async getUserProgress(userId: string): Promise<UserProgress[]> {
    return await db.select().from(userProgress).where(eq(userProgress.userId, userId));
  }

  async updateUserProgress(userId: string, progress: typeof userProgress.$inferInsert): Promise<UserProgress> {
    const existing = await db.select().from(userProgress)
      .where(and(eq(userProgress.userId, userId), eq(userProgress.lessonId, progress.lessonId)))
      .limit(1);

    if (existing.length > 0) {
      const [updated] = await db.update(userProgress)
        .set({ 
          completed: progress.completed,
          score: progress.score,
          lastCode: progress.lastCode,
          completedAt: progress.completed ? new Date() : null,
        })
        .where(eq(userProgress.id, existing[0].id))
        .returning();
      return updated;
    } else {
      const [inserted] = await db.insert(userProgress)
        .values({ ...progress, userId })
        .returning();
      return inserted;
    }
  }

}

export const storage = new DatabaseStorage();
