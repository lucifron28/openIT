<script lang="ts">
  import '../app.css';
  import Sidebar from '$lib/components/Sidebar.svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let sidebarOpen = true;
  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }
  let isAuthPage = false;
  $: {
    const unsubscribe = page.subscribe(($page) => {
      isAuthPage = $page.url.pathname === '/login' || $page.url.pathname === '/register';
    });
  }

  function getCookie(name: string) {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith(name + '='))
      ?.split('=')[1];
  }

  onMount(() => {
    if (!$page.url.pathname.startsWith('/login') && !$page.url.pathname.startsWith('/register')) {
      const accessToken = getCookie('access_token');
      if (!accessToken) {
        window.location.href = '/login';
      }
    }
  });
</script>

{#if isAuthPage}
  <slot />
{:else}
  <div class="flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
    <!-- Sidebar -->
    <Sidebar bind:open={sidebarOpen} />
    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden {sidebarOpen ? 'ml-64' : 'ml-16'} transition-all duration-300">
      <!-- Top bar -->
      <header class="bg-slate-800/50 backdrop-blur-lg border-b border-slate-700/50 px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <button 
              on:click={toggleSidebar}
              class="p-2 rounded-lg hover:bg-slate-700/50 transition-colors"
              aria-label="Toggle sidebar navigation"
            >
              <svg class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
            <h1 class="text-xl font-semibold text-white">
              {#if $page.route.id === '/'} Dashboard
              {:else if $page.route.id === '/tasks'} Tasks
              {:else if $page.route.id === '/team'} Projects
              {:else if $page.route.id === '/achievements'} Achievements
              {:else if $page.route.id === '/coach'} AI Coach
              {:else} AQuest
              {/if}
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2 bg-slate-700/50 rounded-lg px-3 py-2">
              <span class="text-2xl">🧑‍💻</span>
              <div class="text-sm">
                <p class="text-white font-medium">Player</p>
                <p class="text-purple-400">Level 1</p>
              </div>
            </div>
          </div>
        </div>
      </header>
      <!-- Page content -->
      <main class="flex-1 overflow-auto p-6">
        <slot />
      </main>
    </div>
  </div>
{/if}
