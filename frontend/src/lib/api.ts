const fallback_backend_url = "http://localhost:8000";

export const backend_url = (
  process.env.NEXT_PUBLIC_BACKEND_URL ?? fallback_backend_url
).replace(/\/$/, "");

type RequestOptions = {
  body?: Record<string, string>;
  method?: "GET" | "POST";
};

export async function backend_request(path: string, options: RequestOptions = {}) {
  const response = await fetch(`${backend_url}${path}`, {
    method: options.method ?? "GET",
    headers: {
      "Content-Type": "application/json",
    },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const data = await response.json();

  if (!response.ok) {
    throw new Error(JSON.stringify(data, null, 2));
  }

  return data;
}
