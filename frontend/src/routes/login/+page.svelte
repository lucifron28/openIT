<script>
  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

  async function handleLogin() {
    loading = true;
    error = '';
    try {
      const res = await fetch(`${API_BASE_URL}/api/users/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include' // Important for cookies!
      });
      const data = await res.json();
      if (!res.ok) {
        error = data.detail || 'Invalid credentials';
      } else if (data.access) {
        // Cookie is set by backend; no need for localStorage
        window.location.href = '/';
      } else {
        error = 'Unexpected response from server';
      }
    } catch {
      error = 'Network error';
    }
    loading = false;
  }
</script>

<svelte:head>
  <title>Login - Zentry</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
  <form class="glass rounded-xl p-8 w-full max-w-md space-y-6 animate-fade-in-up" on:submit|preventDefault={handleLogin}>
    <h2 class="text-2xl font-bold text-white mb-2 text-center">Login to Zentry</h2>
    {#if error}
      <div class="bg-red-500/20 text-red-300 rounded p-2 text-center">{error}</div>
    {/if}
    <div>
      <label class="block text-gray-300 mb-1" for="email">Email</label>
      <input id="email" type="email" class="w-full p-3 rounded bg-slate-700/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" bind:value={email} required />
    </div>
    <div>
      <label class="block text-gray-300 mb-1" for="password">Password</label>
      <input id="password" type="password" class="w-full p-3 rounded bg-slate-700/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" bind:value={password} required />
    </div>
    <button class="w-full btn-glow bg-gradient-to-r from-purple-500/20 to-teal-500/20 border border-purple-500/30 rounded-lg p-3 text-white font-semibold hover:bg-gradient-to-r hover:from-purple-500/30 hover:to-teal-500/30 transition-all" type="submit" disabled={loading}>
      {loading ? 'Logging in...' : 'Login'}
    </button>
    <p class="text-gray-400 text-center text-sm">
      Don't have an account? <a href="/register" class="text-gradient-purple-teal font-medium">Register</a>
    </p>
  </form>
</div>