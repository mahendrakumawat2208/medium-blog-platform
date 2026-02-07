"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api, type Post } from "@/lib/api";

function formatDate(s: string) {
  return new Date(s).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

export default function PostPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    api.posts
      .getBySlug(slug)
      .then(setPost)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <div className="py-12 text-center text-zinc-500">Loading…</div>;
  if (error || !post) {
    return (
      <div className="py-12 text-center">
        <p className="text-zinc-600 dark:text-zinc-400">{error || "Post not found."}</p>
        <Link href="/" className="mt-4 inline-block text-sm underline">Back to home</Link>
      </div>
    );
  }

  const name = post.author?.display_name || post.author?.username || "Anonymous";

  return (
    <article className="py-8">
      <header className="mb-8">
        <h1 className="font-serif text-4xl font-bold text-zinc-900 dark:text-zinc-50">
          {post.title}
        </h1>
        <div className="mt-4 flex items-center gap-3">
          <Link href={`/profile/${post.author?.username}`} className="flex items-center gap-2">
            {post.author?.avatar_url ? (
              <img
                src={post.author.avatar_url}
                alt=""
                className="h-10 w-10 rounded-full object-cover"
              />
            ) : (
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-zinc-300 text-sm font-medium text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300">
                {(name[0] || "?").toUpperCase()}
              </div>
            )}
            <span className="font-medium text-zinc-900 dark:text-zinc-50">{name}</span>
          </Link>
          <time className="text-zinc-500" dateTime={post.published_at || post.created_at}>
            {formatDate(post.published_at || post.created_at)}
          </time>
        </div>
      </header>
      {post.cover_image_url && (
        <img
          src={post.cover_image_url}
          alt=""
          className="mb-8 w-full rounded-lg object-cover"
        />
      )}
      <div className="prose prose-zinc dark:prose-invert max-w-none whitespace-pre-wrap font-serif text-lg leading-relaxed text-zinc-700 dark:text-zinc-300">
        {post.body}
      </div>
      <p className="mt-12">
        <Link href="/" className="text-sm text-zinc-600 underline dark:text-zinc-400">← Back to home</Link>
      </p>
    </article>
  );
}
