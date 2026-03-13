import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@shared/routes";
import { apiUrl, getAccessToken } from "@/lib/api";
import { userProgress } from "@shared/schema";
type InsertUserProgress = typeof userProgress.$inferInsert;

export function useProgress() {
  return useQuery({
    queryKey: [api.progress.get.path],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(api.progress.get.path), {
        credentials: "include",
        headers: accessToken ? { Authorization: `Bearer ${accessToken}` } : undefined,
      });
      if (!res.ok) throw new Error("Failed to fetch progress");
      return api.progress.get.responses[200].parse(await res.json());
    },
  });
}

export function useUpdateProgress() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: InsertUserProgress) => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(api.progress.update.path), {
        method: api.progress.update.method,
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify(data),
        credentials: "include",
      });
      if (!res.ok) throw new Error("Failed to update progress");
      return api.progress.update.responses[200].parse(await res.json());
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [api.progress.get.path] });
    },
  });
}
