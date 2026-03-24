import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { refreshAndRetry } from "@/lib/api-auth";
import { useAuth } from "@/hooks/use-auth";
import { type UserProgress } from "@/types";

export function useTopicProgress() {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/progress"],
    queryFn: async () => {
      return refreshAndRetry<unknown>((token) =>
        fetch(apiUrl("/api/progress/"), {
          credentials: "include",
          headers: { Authorization: `Bearer ${token}` },
        })
      );
    },
    enabled: isAuthenticated,
  });
}

export function useUserProgress() {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/user-progress"],
    queryFn: async () => {
      return refreshAndRetry<UserProgress[]>((token) =>
        fetch(apiUrl("/api/user-progress/"), {
          credentials: "include",
          headers: { Authorization: `Bearer ${token}` },
        })
      );
    },
    enabled: isAuthenticated,
  });
}

export function useUpdateProgress() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<UserProgress>) => {
      return refreshAndRetry<Partial<UserProgress>>((token) =>
        fetch(apiUrl("/api/user-progress/"), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            lessonId: data.lessonId,
            completed: data.completed || false,
            score: data.score || 0,
            lastCode: data.lastCode || "",
            completedAt: (data as any).completedAt || null,
          }),
          credentials: "include",
        })
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/user-progress"] });
      queryClient.invalidateQueries({ queryKey: ["/api/progress"] });
      queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
      queryClient.invalidateQueries({ queryKey: ["/api/lessons"] });
      queryClient.invalidateQueries({ queryKey: ["/api/modules"] });
    },
  });
}
