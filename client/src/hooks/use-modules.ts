import { useQuery } from "@tanstack/react-query";
import { apiUrl, getAccessToken } from "@/lib/api";
import { useAuth } from "@/hooks/use-auth";
import { type Module, type Lesson } from "@/types";

type ModuleWithLessons = Module & { lessons: Lesson[] };

export function useModules(options?: { enabled?: boolean }) {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/modules"],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl("/api/modules/"), {
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
      return await res.json() as ModuleWithLessons[];
    },
    enabled: (options?.enabled ?? true) && isAuthenticated,
  });
}

export function useModule(id: number) {
  const { isAuthenticated } = useAuth();
  return useQuery({
    queryKey: ["/api/modules", id],
    queryFn: async () => {
      const url = `/api/modules/${id}/`;
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
      return await res.json();
    },
    enabled: !!id && isAuthenticated,
  });
}
