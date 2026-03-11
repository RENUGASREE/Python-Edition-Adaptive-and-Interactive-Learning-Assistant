import { z } from 'zod';
import { 
  insertModuleSchema, 
  insertLessonSchema, 
  insertQuizSchema, 
  insertChallengeSchema,
  insertUserProgressSchema,
  modules,
  lessons,
  quizzes,
  questions,
  challenges,
  userProgress
} from './schema';

export const errorSchemas = {
  validation: z.object({
    message: z.string(),
    field: z.string().optional(),
  }),
  notFound: z.object({
    message: z.string(),
  }),
  internal: z.object({
    message: z.string(),
  }),
};

export const api = {
  modules: {
    list: {
      method: 'GET' as const,
      path: '/api/modules',
      responses: {
        200: z.array(z.custom<typeof modules.$inferSelect & { lessons: (typeof lessons.$inferSelect)[] }>()),
      },
    },
    get: {
      method: 'GET' as const,
      path: '/api/modules/:id',
      responses: {
        200: z.custom<typeof modules.$inferSelect & { lessons: (typeof lessons.$inferSelect)[] }>(),
        404: errorSchemas.notFound,
      },
    },
  },
  lessons: {
    get: {
      method: 'GET' as const,
      path: '/api/lessons/:id',
      responses: {
        200: z.custom<typeof lessons.$inferSelect & { 
          module: typeof modules.$inferSelect,
          quizzes: (typeof quizzes.$inferSelect & { questions: typeof questions.$inferSelect[] })[],
          challenges: typeof challenges.$inferSelect[]
        }>(),
        404: errorSchemas.notFound,
      },
    },
  },
  challenges: {
    run: {
      method: 'POST' as const,
      path: '/api/challenges/:id/run',
      input: z.object({
        code: z.string(),
      }),
      responses: {
        200: z.object({
          output: z.string(),
          error: z.string().nullable().optional(),
          passed: z.boolean(),
        }),
        404: errorSchemas.notFound,
      },
    },
  },
  progress: {
    update: {
      method: 'POST' as const,
      path: '/api/user-progress/',
      input: insertUserProgressSchema,
      responses: {
        200: z.custom<typeof userProgress.$inferSelect>(),
      },
    },
    get: {
      method: 'GET' as const,
      path: '/api/user-progress/',
      responses: {
        200: z.array(z.custom<typeof userProgress.$inferSelect>()),
      },
    },
  },
};

export function buildUrl(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (url.includes(`:${key}`)) {
        url = url.replace(`:${key}`, String(value));
      }
    });
  }
  return url;
}
