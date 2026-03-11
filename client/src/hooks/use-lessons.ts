import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { apiUrl } from "@/lib/api";
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
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl(url), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch lesson");
      return api.lessons.get.responses[200].parse(await res.json());
    },
    enabled: !!id,
  });
}

export function useRunChallenge() {
  return useMutation({
    mutationFn: async ({ id, code }: { id: number; code: string }) => {
      const url = buildUrl(api.challenges.run.path, { id });
      const accessToken = localStorage.getItem("access_token");
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
