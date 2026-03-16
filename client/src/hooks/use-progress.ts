import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useAuth } from "@/hooks/use-auth";
import { type UserProgress } from "@/types";

export function useTopicProgress() {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/progress"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/api/progress/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch topic progress");
      return await res.json();
    },
    enabled: isAuthenticated,
  });
}

export function useUserProgress() {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/user-progress"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/api/user-progress/"), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch user progress");
      return await res.json() as UserProgress[];
    },
    enabled: isAuthenticated,
  });
}

export function useUpdateProgress() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<UserProgress>) => {
      const accessToken = getAccessToken();
      // Using the generic UserProgressViewSet which supports standard POST/create
      const res = await fetch(apiUrl("/api/user-progress/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({
          lessonId: data.lessonId,
          completed: data.completed,
          score: data.score,
          lastCode: data.lastCode,
          timeSpent: (data as any).timeSpent || 0,
          hintsUsed: (data as any).hintsUsed || 0,
        }),
        credentials: "include",
      });
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to update progress: ${res.status} ${errorText}`);
      }
      return await res.json();
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
