import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";
import { refreshAndRetry } from "@/lib/api-auth";

export function useMasteryUpdate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ moduleId, score, source, topic }: { moduleId: string; score: number; source: string; topic?: string | null }) => {
      return refreshAndRetry<unknown>((token) =>
        fetch(apiUrl("/mastery/update"), {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ moduleId, score, source, topic }),
          credentials: "include",
        })
      );
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/metrics"] });
    },
  });
}
