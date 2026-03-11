import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiUrl } from "@/lib/api";


export function useMasteryUpdate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ moduleId, score, source, topic }: { moduleId: number; score: number; source: string; topic?: string | null }) => {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(apiUrl("/mastery/update"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ moduleId, score, source, topic }),
        credentials: "include",
      });
      if (!res.ok) throw new Error("Failed to update mastery");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/metrics"] });
    },
  });
}
