"use client";

import { useEffect, useState } from "react";
import { api, type Post } from "@/lib/api";
import PostCard from "@/components/PostCard";

export default function HomePage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.feed
      .get()
      .then(setPosts)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="py-12 text-center text-zinc-500">Loading stories…</div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-amber-800 dark:border-amber-800 dark:bg-amber-950/30 dark:text-amber-200">
        Could not load feed. Is the API running at{" "}
        {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}?
        <br />
        <span className="text-sm">{error}</span>
      </div>
    );
  }

  if (posts.length === 0) {
    return (
      <div className="py-16 text-center">
        <p className="text-zinc-600 dark:text-zinc-400">No stories yet.</p>
        <p className="mt-2 text-sm text-zinc-500">
          <a href="/write" className="underline hover:no-underline">Write the first one</a>.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="sr-only">Latest stories</h1>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
