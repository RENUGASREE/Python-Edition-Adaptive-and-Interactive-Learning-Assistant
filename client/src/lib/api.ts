export const API_BASE = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/+$/, "");

export function apiUrl(path: string): string {
  const clean = path.replace(/^https?:\/\/[^/]+/i, "").replace(/^\/+/, "");
  if (clean.startsWith("api/")) {
    return `${API_BASE}/${clean.slice(4)}`;
  }
  return `${API_BASE}/${clean}`;
}

export function withParams(path: string, params?: Record<string, string | number>): string {
  let url = path;
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url = url.replace(`:${key}`, String(value));
    });
  }
  return apiUrl(url);
}
