export interface User {
  id: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  has_taken_quiz: boolean;
  diagnostic_completed: boolean;
  mastery_vector: Record<string, number>;
  engagement_score: number;
  level?: string;
}

export interface Module {
  id: number;
  title: string;
  description: string;
  order: number;
}

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  content: string;
  order: number;
  duration: number;
  slug: string;
  difficulty: string;
}

export interface Quiz {
  id: number;
  lesson_id: number;
  title: string;
}

export interface Question {
  id: number;
  quiz_id: number;
  text: string;
  type: string;
  options: any[];
  points: number;
}

export interface Challenge {
  id: number;
  lesson_id: number;
  title: string;
  description: string;
  initial_code: string;
  solution_code: string | null;
  test_cases: any[];
  points: number;
}

export interface UserProgress {
  id: number;
  userId: string;
  lessonId: number;
  completed: boolean;
  score: number;
  lastCode?: string;
  completedAt?: string;
}
