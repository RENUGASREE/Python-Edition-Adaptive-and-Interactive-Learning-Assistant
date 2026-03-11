export type BatchOptions = {
  concurrency?: number;
};

export function isRateLimitError(_e: unknown): boolean {
  return false;
}

export async function batchProcess<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  _options?: BatchOptions,
): Promise<R[]> {
  return Promise.all(items.map(fn));
}

export async function batchProcessWithSSE<T, R>(
  items: T[],
  fn: (item: T) => Promise<R>,
  onChunk: (chunk: string) => void,
  _options?: BatchOptions,
): Promise<R[]> {
  const results: R[] = [];
  for (const item of items) {
    const res = await fn(item);
    results.push(res);
    onChunk(typeof res === "string" ? res : JSON.stringify(res));
  }
  return results;
}
