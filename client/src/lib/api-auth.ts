import { apiUrl, getAccessToken, getRefreshToken, storeTokens } from "./api";

/**
 * Helper function to handle API calls with automatic token refresh.
 * When a 401 is received and a refresh token is available, it will:
 * 1. Attempt to refresh the access token
 * 2. Retry the original request with the new token
 * 3. Return the response or throw an error
 */
export async function refreshAndRetry<T>(
  fn: (token: string) => Promise<Response>,
): Promise<T> {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();

  if (!accessToken) {
    throw new Error("No access token available");
  }

  let response = await fn(accessToken);

  // If 401 and we have a refresh token, try to refresh
  if (response.status === 401 && refreshToken) {
    try {
      const refreshResponse = await fetch(apiUrl("/token/refresh/"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
        credentials: "include",
      });

      if (refreshResponse.ok) {
        const data = await refreshResponse.json();
        if (data?.access) {
          storeTokens(data.access, data.refresh ?? refreshToken);
          // Retry the original request with new token
          response = await fn(data.access);
        }
      }
    } catch (error) {
      console.error("Token refresh failed:", error);
    }
  }

  if (!response.ok) {
    const text = await response.text();
    console.error("Request failed:", response.status, text);
    let message = `Server Error (${response.status}): ${text || "No response body"}`;
    try {
      const json = JSON.parse(text);
      if (json?.detail) message = json.detail;
      else if (json?.message) message = json.message;
      else if (json?.error) message = json.error;
    } catch {
      // Keep descriptive message
    }
    throw new Error(message);
  }

  return await response.json() as T;
}
