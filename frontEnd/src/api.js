

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function apiRequest(endpoint, body) {
  const res = await fetch(`${API_BASE}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  let data = {};
  try {
    data = await res.json();
  } catch {
    // ignore non-JSON responses
  }
  const message = data.detail || data.message || JSON.stringify(data);
  return { ok: res.ok, message };
}
