export const API_BASE = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/+$/, "");

export function apiUrl(path: string): string {
  const clean = path.replace(/^https?:\/\/[^/]+/i, "").replace(/^\/+/, "");
  const result = clean.startsWith("api/")
    ? `${API_BASE}/${clean.slice(4)}`
    : `${API_BASE}/${clean}`;

  // Ensure API routes have a trailing slash to avoid Django redirects that can strip
  // Authorization headers on cross-origin redirects.
  // Preserve query strings / fragments when adding the trailing slash.
  const match = result.match(/^(?<base>[^?#]*)(?<suffix>[?#].*)?$/);
  if (!match) return result;

  const base = match.groups?.base ?? result;
  const suffix = match.groups?.suffix ?? "";
  const baseWithSlash = base.endsWith("/") ? base : `${base}/`;
  return `${baseWithSlash}${suffix}`;
}

export function getAccessToken(): string | null {
  // Support both old (`token`) and current (`access_token`) keys for backwards compatibility.
  return (
    localStorage.getItem("access_token") ||
    localStorage.getItem("token") ||
    null
  );
}

export function getRefreshToken(): string | null {
  return (
    localStorage.getItem("refresh_token") ||
    localStorage.getItem("refresh") ||
    null
  );
}

export function clearTokens(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("token");
  localStorage.removeItem("refresh");
}

export function storeTokens(access: string, refresh: string): void {
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
  localStorage.setItem("token", access);
  localStorage.setItem("refresh", refresh);
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
