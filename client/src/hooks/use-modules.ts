import { useQuery } from "@tanstack/react-query";
import { api, buildUrl } from "@shared/routes";
import { apiUrl, getAccessToken } from "@/lib/api";
import { type Module, type Lesson } from "@shared/schema";

type ModuleWithLessons = Module & { lessons: Lesson[] };

export function useModules(options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: [api.modules.list.path],
    queryFn: async () => {
      const accessToken = getAccessToken();
      const res = await fetch(apiUrl(api.modules.list.path), {
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
      return api.modules.list.responses[200].parse(await res.json()) as ModuleWithLessons[];
    },
    enabled: options?.enabled ?? true,
  });
}

export function useModule(id: number) {
  return useQuery({
    queryKey: [api.modules.get.path, id],
    queryFn: async () => {
      const url = buildUrl(api.modules.get.path, { id });
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
      return api.modules.get.responses[200].parse(await res.json());
    },
    enabled: !!id,
  });
}
