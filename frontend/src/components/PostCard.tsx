import Link from "next/link";
import type { Post } from "@/lib/api";

function formatDate(s: string) {
  return new Date(s).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export default function PostCard({ post }: { post: Post }) {
  const name = post.author?.display_name || post.author?.username || "Anonymous";

  return (
    <article className="group border-b border-zinc-200 py-8 dark:border-zinc-800">
      <Link href={`/profile/${post.author?.username}`} className="mb-2 flex items-center gap-2">
        {post.author?.avatar_url ? (
          <img
            src={post.author.avatar_url}
            alt=""
            className="h-8 w-8 rounded-full object-cover"
          />
        ) : (
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-zinc-300 text-xs font-medium text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300">
            {(name[0] || "?").toUpperCase()}
          </div>
        )}
        <span className="text-sm text-zinc-600 dark:text-zinc-400">{name}</span>
      </Link>
      <Link href={`/post/${post.slug}`} className="block">
        <h2 className="font-serif text-2xl font-bold text-zinc-900 group-hover:text-zinc-600 dark:text-zinc-50 dark:group-hover:text-zinc-300">
          {post.title}
        </h2>
        <p className="mt-1 line-clamp-2 text-zinc-600 dark:text-zinc-400">
          {post.body.slice(0, 160)}
          {post.body.length > 160 ? "…" : ""}
        </p>
        <time className="mt-2 block text-sm text-zinc-500" dateTime={post.published_at || post.created_at}>
          {formatDate(post.published_at || post.created_at)}
        </time>
      </Link>
    </article>
  );
}
