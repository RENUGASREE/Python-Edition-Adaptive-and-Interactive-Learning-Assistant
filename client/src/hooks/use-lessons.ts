import { useQuery, useMutation } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
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
      const url = `/api/lessons/${id}/`;
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
      return await res.json() as LessonResponse;
    },
    enabled: !!id && isAuthenticated,
  });
}

export function useRunChallenge() {
  return useMutation({
    mutationFn: async ({ id, code }: { id: number; code: string }) => {
      const url = `/api/challenges/${id}/run/`;
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(url), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ code }),
        credentials: "include",
      });
      
      if (!res.ok) {
        const text = await res.text();
        console.error("Code execution failed:", res.status, text);
        let message = `Server Error (${res.status}): ${text || "No response body"}`;
        try {
          const json = JSON.parse(text);
          if (json?.message) message = json.message;
          else if (json?.error) message = json.error;
        } catch {
          // If not JSON, we'll keep the descriptive message with status and body
        }
        throw new Error(message);
      }
      return await res.json();
    },
  });
}
