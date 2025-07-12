<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  export let open = true;

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

  const navigation = [
    { name: 'Dashboard', href: '/', icon: '📊', emoji: '🏠' },
    { name: 'Tasks', href: '/tasks', icon: '📝', emoji: '✅' },
    { name: 'Projects', href: '/team', icon: '👥', emoji: '🤝' },
    { name: 'Achievements', href: '/achievements', icon: '🏆', emoji: '🎖️' },
    { name: 'AI Coach', href: '/coach', icon: '🤖', emoji: '💡' },
    { name: 'Settings', href: '/settings', icon: '⚙️', emoji: '🔧' },
  ];

  $: currentPath = $page.url.pathname;

  let user = {
    id: null,
    currentStreak: 0,
    experience: 0,
    experienceToNext: 100,
    level: 1,
    avatar: '👤',
    points: 0,
    username: ''
  };
  let loadingUser = true;

  onMount(async () => {
    try {

      const res = await fetch(`${API_BASE_URL}/api/users/me/`, { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        user.currentStreak = data.currentStreak ?? 0;
        user.experience = data.experience ?? 0;
        user.experienceToNext = data.experienceToNext ?? 100;
        user.level = data.level ?? 1;
        user.avatar = data.avatar || '👤';
        user.points = data.points ?? 0;
        user.username = data.username ?? '';
        user.id = data.id ?? null;
      }
    } finally {
      loadingUser = false;
    }
  });

  $: xpPercent = Math.min(100, Math.round((user.experience / user.experienceToNext) * 100));

  async function logout() {
    try {
      await fetch(`${API_BASE_URL}/api/users/logout/`, {
        method: 'POST',
        credentials: 'include'
      });
      document.cookie = 'access_token=; Max-Age=0; path=/';
      document.cookie = 'refresh_token=; Max-Age=0; path=/api/token/refresh/';
      window.location.href = '/login';
    } catch (e) {
      window.location.href = '/login';
    }
  }
</script>

<aside class="fixed left-0 inset-y-0 h-screen {open ? 'w-64' : 'w-16'} bg-slate-800/50 backdrop-blur-lg border-r border-slate-700/50 transition-all duration-300 z-40 flex flex-col">
  <div class="p-6 border-b border-slate-700/50">
    <div class="flex items-center space-x-3">
      <img
        src="../src/assets/aquest-logo.png"
        alt="Aquest Logo"
        class="w-10 h-10 rounded-lg object-cover"
        draggable="false"
      >
      {#if open}
        <div>
          <h2 class="text-xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">AQuest</h2>
          <p class="text-xs text-gray-400">Level Up Productivity</p>
        </div>
      {/if}
    </div>
  </div>
  <nav class="flex-1 p-4">
    <ul class="space-y-2">
      {#each navigation as item}
        <li>
          <a 
            href={item.href}
            class="flex items-center space-x-3 p-3 rounded-lg transition-all duration-200 group
              {currentPath === item.href 
                ? 'bg-gradient-to-r from-purple-500/20 to-teal-500/20 text-white border border-purple-500/30' 
                : 'text-gray-300 hover:bg-slate-700/50 hover:text-white'
              }"
          >
            <span class="text-xl group-hover:animate-bounce-slow">
              {currentPath === item.href ? item.emoji : item.icon}
            </span>
            {#if open}
              <span class="font-medium">{item.name}</span>
              {#if currentPath === item.href}
                <div class="ml-auto w-2 h-2 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full animate-pulse-slow"></div>
              {/if}
            {/if}
          </a>
        </li>
      {/each}
    </ul>
  </nav>
  {#if open}
    <div class="p-4 border-t border-slate-700/50">
      <div class="bg-gradient-to-r from-purple-500/10 to-teal-500/10 rounded-lg p-4 space-y-3">
        {#if loadingUser}
          <div class="text-gray-400 text-center">Loading…</div>
        {:else}
          <div class="flex items-center justify-between mb-1">
            <span class="flex items-center gap-2">
              <span class="text-2xl">{user.avatar}</span>
              <span class="text-white font-semibold">@{user.username}</span>
            </span>
            <span class="text-xs bg-slate-700 px-2 py-1 rounded text-purple-300">Level {user.level}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-300">Current Streak</span>
            <div class="flex items-center space-x-1">
              <span class="text-orange-400">🔥</span>
              <span class="text-white font-semibold">{user.currentStreak} day{user.currentStreak === 1 ? '' : 's'}</span>
            </div>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-300">Points</span>
            <span class="text-teal-300 font-bold">{user.points}</span>
          </div>
        {/if}
      </div>
    </div>
  {/if}
  <div class="p-4 border-t border-slate-700/50">
    <button
      on:click={logout}
      class="cursor-pointer w-full flex items-center justify-center gap-3 px-4 py-2 rounded-lg
        bg-transparent text-gray-300 font-medium transition-all duration-200
        hover:bg-slate-700/50 hover:text-white focus:outline-none"
      style="outline: none;"
    >
      <span class="text-xl">🚪</span>
      {#if open}
        <span>Logout</span>
      {/if}
    </button>
  </div>
</aside>
