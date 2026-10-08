// --- API URL resolution (in priority order) ---
//   1. VITE_API_URL from .env       (used on GitHub Pages / production)
//   2. Auto-detect from Codespaces  (e.g. -5173. -> -8000.)
//   3. Localhost fallback           (npm run dev on your own machine)
function getApiUrl(): string {
  const fromEnv = import.meta.env.VITE_API_URL as string | undefined;
  if (fromEnv && fromEnv.length > 0) return fromEnv;

  const origin = window.location.origin;
  const match = origin.match(/-(\d+)\./);
  if (match) return origin.replace(`-${match[1]}.`, "-8000.");

  return "http://localhost:8000";
}

const API_URL = getApiUrl();

export function getToken(): string | null {
  return localStorage.getItem("mesh_token");
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem("mesh_token", token);
  else localStorage.removeItem("mesh_token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    ...((options.headers as Record<string, string>) || {}),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  const text = await res.text();
  let data: any = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!res.ok) {
    const msg = data?.detail || data?.message || `HTTP ${res.status}`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return data as T;
}

// ---------- Auth ----------
export async function register(email: string, password: string) {
  const data = await request<{ access_token: string }>(
    "/api/auth/register",
    { method: "POST", body: JSON.stringify({ email, password }) }
  );
  setToken(data.access_token);
  return data;
}

export async function login(email: string, password: string) {
  const data = await request<{ access_token: string }>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  setToken(data.access_token);
  return data;
}

export function logout() {
  setToken(null);
}

// ---------- Upload ----------
export async function uploadImage(
  file: File,
  prompt: string,
  quality: string
): Promise<{ job_id: string; status: string; message: string }> {
  const form = new FormData();
  form.append("file", file);
  form.append("prompt", prompt);
  form.append("quality", quality);
  return request("/api/upload", { method: "POST", body: form });
}

// ---------- Jobs ----------
export interface Job {
  id: string;
  status: string;
  stage?: string | null;
  progress?: number;
  error?: string | null;
  prompt?: string;
  quality?: string;
  created_at?: string;
}

export async function listJobs(): Promise<Job[]> {
  return request<Job[]>("/api/jobs");
}

export async function getJob(jobId: string): Promise<Job> {
  return request<Job>(`/api/jobs/${jobId}`);
}

export const API_BASE = API_URL;
