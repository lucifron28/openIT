<script>
  import { onMount } from 'svelte';
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

  let user = {
    name: '...',
    level: 1,
    experience: 0,
    experienceToNext: 100,
    currentStreak: 0,
    avatar: '🧑‍💻'
  };

  onMount(async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/users/me/`, { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        user = {
          ...user,
          name: data.username || 'User',
          avatar: data.avatar || '🧑‍💻',
          level: data.level ?? 1,
          experience: data.experience ?? 0,
          experienceToNext: data.experienceToNext ?? 100,
          currentStreak: data.currentStreak ?? 0
        };
      }
    } catch {}
  });

  let taskStats = { todo: 8, inProgress: 3, completed: 15 };
  let currentProject = { name: 'AQuest Development', emoji: '🚀', progress: 65 };
  let recentActivity = [
    { action: 'Completed task', task: 'Set up authentication', time: '2 hours ago', emoji: '✅' },
    { action: 'Started task', task: 'Design dashboard UI', time: '4 hours ago', emoji: '🎨' },
    { action: 'Earned badge', task: 'Task Master', time: '1 day ago', emoji: '🏆' },
    { action: 'Level up!', task: 'Reached Level 3', time: '2 days ago', emoji: '🌟' }
  ];

  $: experiencePercentage = (user.experience / user.experienceToNext) * 100;
</script>

<svelte:head>
  <title>Dashboard - AQuest</title>
</svelte:head>

<div class="space-y-6">
  <div class="glass rounded-xl p-6 animate-fade-in-up">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-white mb-2">
          Welcome back, <span class="text-gradient-purple-teal">{user.name}</span>! 👋
        </h1>
        <p class="text-gray-300">Ready to level up your productivity today?</p>
      </div>
      <div class="text-6xl animate-bounce-slow">{user.avatar}</div>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="glass rounded-xl p-6 animate-fade-in-up">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Level Progress</h3>
        <span class="text-2xl">🌟</span>
      </div>
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-2xl font-bold text-gradient-blue">Level {user.level}</span>
          <span class="text-sm text-gray-400">{user.experience}/{user.experienceToNext} XP</span>
        </div>
        <div class="w-full bg-slate-700 rounded-full h-3">
          <div 
            class="bg-gradient-to-r from-purple-500 to-teal-500 h-3 rounded-full transition-all duration-1000 animate-pulse-slow" 
            style="width: {experiencePercentage}%"
          ></div>
        </div>
        <p class="text-sm text-gray-400">{user.experienceToNext - user.experience} XP to next level</p>
      </div>
    </div>

    <div class="glass rounded-xl p-6 animate-fade-in-up">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Current Streak</h3>
        <span class="text-2xl animate-pulse-slow">🔥</span>
      </div>
      <div class="text-center">
        <div class="text-4xl font-bold text-gradient-purple-teal mb-2">{user.currentStreak}</div>
        <p class="text-gray-300">days in a row!</p>
        <p class="text-sm text-gray-400 mt-2">Keep it up! 💪</p>
      </div>
    </div>

    <div class="glass rounded-xl p-6 animate-fade-in-up">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Active Project</h3>
        <span class="text-2xl">{currentProject.emoji}</span>
      </div>
      <div class="space-y-3">
        <h4 class="font-semibold text-white">{currentProject.name}</h4>
        <div class="flex items-center justify-between">
          <span class="text-sm text-gray-400">Progress</span>
          <span class="text-sm font-medium text-white">{currentProject.progress}%</span>
        </div>
        <div class="w-full bg-slate-700 rounded-full h-2">
          <div 
            class="bg-gradient-to-r from-purple-500 to-teal-500 h-2 rounded-full transition-all duration-1000" 
            style="width: {currentProject.progress}%"
          ></div>
        </div>
      </div>
    </div>

    <div class="glass rounded-xl p-6 animate-fade-in-up">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-white">Task Status</h3>
        <span class="text-2xl">📊</span>
      </div>
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-gray-300">To Do</span>
          <span class="px-2 py-1 bg-gray-600 rounded-full text-sm font-medium">{taskStats.todo}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-gray-300">In Progress</span>
          <span class="px-2 py-1 bg-yellow-600 rounded-full text-sm font-medium">{taskStats.inProgress}</span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-gray-300">Completed</span>
          <span class="px-2 py-1 bg-green-600 rounded-full text-sm font-medium">{taskStats.completed}</span>
        </div>
      </div>
    </div>
  </div>

  <div class="glass rounded-xl p-6 animate-fade-in-up">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-semibold text-white">Recent Activity</h3>
      <span class="text-2xl">⚡</span>
    </div>
    <div class="space-y-4">
      {#each recentActivity as activity}
        <div class="flex items-center space-x-4 p-3 rounded-lg hover:bg-slate-700/30 transition-colors">
          <span class="text-xl">{activity.emoji}</span>
          <div class="flex-1">
            <p class="text-white">
              <span class="font-medium">{activity.action}</span>
              {#if activity.task}
                <span class="text-gray-300">: {activity.task}</span>
              {/if}
            </p>
            <p class="text-sm text-gray-400">{activity.time}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <div class="glass rounded-xl p-6 animate-fade-in-up">
    <h3 class="text-xl font-semibold text-white mb-6">Quick Actions</h3>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <button class="btn-glow bg-gradient-to-r from-purple-500/20 to-teal-500/20 border border-purple-500/30 rounded-lg p-4 text-left hover:bg-gradient-to-r hover:from-purple-500/30 hover:to-teal-500/30 transition-all">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">➕</span>
          <div>
            <h4 class="font-semibold text-white">Add New Task</h4>
            <p class="text-sm text-gray-400">Create a new task to work on</p>
          </div>
        </div>
      </button>
      <button class="btn-glow-teal bg-gradient-to-r from-teal-500/20 to-purple-500/20 border border-teal-500/30 rounded-lg p-4 text-left hover:bg-gradient-to-r hover:from-teal-500/30 hover:to-purple-500/30 transition-all">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">👥</span>
          <div>
            <h4 class="font-semibold text-white">View Team</h4>
            <p class="text-sm text-gray-400">Check your team's progress</p>
          </div>
        </div>
      </button>
      <button class="btn-glow bg-gradient-to-r from-purple-500/20 to-teal-500/20 border border-purple-500/30 rounded-lg p-4 text-left hover:bg-gradient-to-r hover:from-purple-500/30 hover:to-teal-500/30 transition-all">
        <div class="flex items-center space-x-3">
          <span class="text-2xl">🤖</span>
          <div>
            <h4 class="font-semibold text-white">Ask Zenturion</h4>
            <p class="text-sm text-gray-400">Get AI coaching advice</p>
          </div>
        </div>
      </button>
    </div>
  </div>
</div>
