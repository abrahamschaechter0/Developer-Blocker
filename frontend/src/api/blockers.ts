export type Status = 'open' | 'in_progress' | 'resolved';
export type Blocker = { id: number; developer: string; title: string; description: string; status: Status };
export type NewBlocker = Pick<Blocker, 'developer' | 'title' | 'description'>;

// Set EXPO_PUBLIC_API_URL in frontend/.env to your computer's reachable address.
const API_URL = (process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000').replace(/\/$/, '');

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Request failed (${response.status}): ${body}`);
  }
  return response.json() as Promise<T>;
}

export async function listBlockers(): Promise<Blocker[]> {
  return request<Blocker[]>('/blockers');
}

export const getBlocker = (id: number) => request<Blocker>(`/blockers/${id}`);
export const createBlocker = (data: NewBlocker) => request<Blocker>('/blockers', { method: 'POST', body: JSON.stringify(data) });
export const updateStatus = (id: number, status: Status) => request<Blocker>(`/blockers/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) });
