"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { api, type User, type Post } from "@/lib/api";
import PostCard from "@/components/PostCard";

export default function ProfilePage() {
  const params = useParams();
  const username = params.username as string;
  const { user: currentUser } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [following, setFollowing] = useState(false);
  const [followLoading, setFollowLoading] = useState(false);

  const isOwnProfile = currentUser?.username === username;

  useEffect(() => {
    if (!username) return;
    api.users
      .getByUsername(username)
      .then((u) => {
        setUser(u);
        return api.users.getPosts(u.id);
      })
      .then(setPosts)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [username]);

  async function toggleFollow() {
    if (!user || !currentUser || followLoading) return;
    setFollowLoading(true);
    try {
      if (following) {
        await api.users.unfollow(user.id);
        setFollowing(false);
      } else {
        await api.users.follow(user.id);
        setFollowing(true);
      }
    } finally {
      setFollowLoading(false);
    }
  }

  if (loading) return <div className="py-12 text-center text-zinc-500">Loading…</div>;
  if (error || !user) {
    return (
      <div className="py-12 text-center">
        <p className="text-zinc-600 dark:text-zinc-400">{error || "User not found."}</p>
        <Link href="/" className="mt-4 inline-block text-sm underline">Back to home</Link>
      </div>
    );
  }

  const displayName = user.display_name || user.username;

  return (
    <div className="py-8">
      <div className="flex flex-col items-start gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          {user.avatar_url ? (
            <img
              src={user.avatar_url}
              alt=""
              className="h-20 w-20 rounded-full object-cover"
            />
          ) : (
            <div className="flex h-20 w-20 items-center justify-center rounded-full bg-zinc-300 text-2xl font-medium text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300">
              {(displayName[0] || "?").toUpperCase()}
            </div>
          )}
          <div>
            <h1 className="font-serif text-2xl font-bold text-zinc-900 dark:text-zinc-50">
              {displayName}
            </h1>
            <p className="text-zinc-600 dark:text-zinc-400">@{user.username}</p>
            {user.bio && (
              <p className="mt-2 max-w-md text-sm text-zinc-600 dark:text-zinc-400">{user.bio}</p>
            )}
          </div>
        </div>
        {currentUser && !isOwnProfile && (
          <button
            type="button"
            onClick={toggleFollow}
            disabled={followLoading}
            className="rounded-full border border-zinc-300 px-5 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50 disabled:opacity-60 dark:border-zinc-600 dark:text-zinc-300 dark:hover:bg-zinc-800"
          >
            {followLoading ? "…" : following ? "Following" : "Follow"}
          </button>
        )}
        {isOwnProfile && (
          <Link
            href="/write"
            className="rounded-full bg-zinc-900 px-5 py-2 text-sm font-medium text-white hover:bg-zinc-800 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            Write
          </Link>
        )}
      </div>
      <section className="mt-12">
        <h2 className="mb-6 font-serif text-xl font-semibold text-zinc-900 dark:text-zinc-50">
          Stories
        </h2>
        {posts.length === 0 ? (
          <p className="text-zinc-500">No published stories yet.</p>
        ) : (
          <div className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {posts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
