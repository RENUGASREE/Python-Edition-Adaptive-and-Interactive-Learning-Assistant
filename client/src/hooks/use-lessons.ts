import { useQuery, useMutation } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { refreshAndRetry } from "@/lib/api-auth";
import { useAuth } from "@/hooks/use-auth";
import { type Lesson, type Quiz, type Question, type Challenge } from "@/types";

type LessonResponse = Lesson & {
  module: { title: string };
  quizzes: (Quiz & { questions: Question[] })[];
  challenges: Challenge[];
};


export function useLesson(id: number) {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/lessons", id],
    queryFn: async () => {
      return refreshAndRetry<LessonResponse>((token) =>
        fetch(apiUrl(`/api/lessons/${id}/`), {
          credentials: "include",
          headers: { Authorization: `Bearer ${token}` },
        })
      );
    },
    enabled: !!id && isAuthenticated,
  });
}

export function useRunChallenge() {
  return useMutation({
    mutationFn: async ({ id, code, input }: { id: number; code: string; input?: string }) => {
      return refreshAndRetry<{ output?: string; error?: string; result?: unknown }>((token) =>
        fetch(apiUrl(`/api/challenges/${id}/run/`), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ code, input: input || "" }),
          credentials: "include",
        })
      );
    },
  });
}
