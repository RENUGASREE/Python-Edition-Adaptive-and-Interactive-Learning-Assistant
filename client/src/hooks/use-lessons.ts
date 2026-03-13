import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { apiUrl, getAccessToken } from "@/lib/api";
import { type Lesson, type Quiz, type Question, type Challenge } from "@shared/schema";

type LessonResponse = Lesson & {
  module: { title: string };
  quizzes: (Quiz & { questions: Question[] })[];
  challenges: Challenge[];
};

export function useLesson(id: number) {
  return useQuery({
    queryKey: [api.lessons.get.path, id],
    queryFn: async () => {
      const url = buildUrl(api.lessons.get.path, { id });
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(url), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });

      if (!res.ok) {
        const text = await res.text();
        let message = res.statusText;
        try {
          const json = JSON.parse(text);
          if (json?.message) message = json.message;
        } catch {
          if (text) message = text;
        }
        const error = new Error(message) as Error & { status?: number };
        error.status = res.status;
        throw error;
      }
      return api.lessons.get.responses[200].parse(await res.json());
    },
    enabled: !!id,
  });
}

export function useRunChallenge() {
  return useMutation({
    mutationFn: async ({ id, code }: { id: number; code: string }) => {
      const url = buildUrl(api.challenges.run.path, { id });
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(url), {
        method: api.challenges.run.method,
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ code }),
        credentials: "include",
      });
      
      if (!res.ok) throw new Error("Failed to run code");
      return api.challenges.run.responses[200].parse(await res.json());
    },
  });
}
