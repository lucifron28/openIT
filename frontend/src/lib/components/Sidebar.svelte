<script>
  import { page } from '$app/stores';
  
  export let open = true;
  
  const navigation = [
    { name: 'Dashboard', href: '/', icon: '📊', emoji: '🏠' },
    { name: 'Tasks', href: '/tasks', icon: '📝', emoji: '✅' },
    { name: 'Team', href: '/team', icon: '👥', emoji: '🤝' },
    { name: 'Achievements', href: '/achievements', icon: '🏆', emoji: '🎖️' },
    { name: 'AI Coach', href: '/coach', icon: '🤖', emoji: '💡' },
    { name: 'Settings', href: '/settings', icon: '⚙️', emoji: '🔧' },
  ];
  
  $: currentPath = $page.url.pathname;
</script>

<aside class="fixed left-0 top-0 h-full {open ? 'w-64' : 'w-16'} bg-slate-800/50 backdrop-blur-lg border-r border-slate-700/50 transition-all duration-300 z-40">
  <div class="flex flex-col h-full">
    <!-- Logo -->
    <div class="p-6 border-b border-slate-700/50">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-teal-500 rounded-lg flex items-center justify-center">
          <span class="text-white font-bold text-lg">Z</span>
        </div>
        {#if open}
          <div>
            <h2 class="text-xl font-bold text-gradient-purple-teal">Zentry</h2>
            <p class="text-xs text-gray-400">Level Up Productivity</p>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Navigation -->
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
    
    <!-- User Stats (when expanded) -->
    {#if open}
      <div class="p-4 border-t border-slate-700/50">
        <div class="bg-gradient-to-r from-purple-500/10 to-teal-500/10 rounded-lg p-4 space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-300">Current Streak</span>
            <div class="flex items-center space-x-1">
              <span class="text-orange-400">🔥</span>
              <span class="text-white font-semibold">5 days</span>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-300">Level Progress</span>
            <span class="text-white font-semibold">XP 250/500</span>
          </div>
          
          <div class="w-full bg-slate-700 rounded-full h-2">
            <div class="bg-gradient-to-r from-purple-500 to-teal-500 h-2 rounded-full" style="width: 50%"></div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</aside>
