const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type User = {
  id: string;
  email: string;
  username: string;
  display_name: string | null;
  bio: string | null;
  avatar_url: string | null;
  created_at: string;
};

export type PostAuthor = {
  id: string;
  username: string;
  display_name: string | null;
  avatar_url: string | null;
};

export type Post = {
  id: string;
  author_id: string;
  author: PostAuthor | null;
  title: string;
  slug: string;
  body: string;
  body_format: string;
  cover_image_url: string | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  user: User;
};

async function getToken(): Promise<string | null> {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getToken();
  const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;

  const res = await fetch(url, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const message =
      typeof err.detail === "string"
        ? err.detail
        : Array.isArray(err.detail) && err.detail[0]
          ? (err.detail[0].msg || String(err.detail[0]))
          : res.statusText;
    throw new Error(message || "Request failed");
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  auth: {
    register: (data: { email: string; password: string; username: string }) =>
      request<TokenResponse>("/auth/register", { method: "POST", body: JSON.stringify(data) }),
    login: (data: { email: string; password: string }) =>
      request<TokenResponse>("/auth/login", { method: "POST", body: JSON.stringify(data) }),
    me: () => request<User>("/auth/me"),
  },
  users: {
    getByUsername: (username: string) => request<User>(`/users/by-username/${username}`),
    getPosts: (userId: string, offset = 0, limit = 20) =>
      request<Post[]>(`/users/${userId}/posts?offset=${offset}&limit=${limit}`),
    follow: (userId: string) => request<void>(`/users/me/follow/${userId}`, { method: "POST" }),
    unfollow: (userId: string) => request<void>(`/users/me/follow/${userId}`, { method: "DELETE" }),
    updateMe: (data: { display_name?: string; bio?: string; avatar_url?: string }) =>
      request<User>("/users/me", { method: "PATCH", body: JSON.stringify(data) }),
  },
  posts: {
    list: (params?: { author_id?: string; offset?: number; limit?: number }) => {
      const sp = new URLSearchParams();
      if (params?.author_id) sp.set("author_id", params.author_id);
      if (params?.offset != null) sp.set("offset", String(params.offset));
      if (params?.limit != null) sp.set("limit", String(params.limit));
      return request<Post[]>(`/posts?${sp}`);
    },
    getBySlug: (slug: string) => request<Post>(`/posts/slug/${slug}`),
    get: (id: string) => request<Post>(`/posts/${id}`),
    create: (data: { title: string; body: string; body_format?: string; cover_image_url?: string; published?: boolean }) =>
      request<Post>("/posts", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: { title?: string; body?: string; body_format?: string; cover_image_url?: string; published?: boolean }) =>
      request<Post>(`/posts/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    delete: (id: string) => request<void>(`/posts/${id}`, { method: "DELETE" }),
  },
  feed: {
    get: (offset = 0, limit = 20) => request<Post[]>(`/feed?offset=${offset}&limit=${limit}`),
  },
};
