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
  id: string;
  title: string;
  description: string;
  order: number;
}

export interface Lesson {
  id: string;
  module_id: string;
  title: string;
  content: string;
  order: number;
  duration: number;
  slug: string;
  difficulty: string;
}

export interface Quiz {
  id: string;
  lesson_id: string;
  title: string;
}

export interface Question {
  id: string;
  quiz_id: string;
  text: string;
  type: string;
  options: any[];
  points: number;
}

export interface Challenge {
  id: string;
  lesson_id: string;
  title: string;
  description: string;
  initial_code: string;
  solution_code: string | null;
  test_cases: any[];
  points: number;
}

export interface UserProgress {
  id: string;
  userId: string;
  lessonId: string;
  completed: boolean;
  quizCompleted?: boolean;
  challengeCompleted?: boolean;
  score: number;
  lastCode?: string;
  completedAt?: string;
}
