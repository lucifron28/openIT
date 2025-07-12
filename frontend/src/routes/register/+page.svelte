<script>
  let username = '';
  let password = '';
  let confirm = '';
  let error = '';
  let loading = false;

  async function handleRegister() {
    loading = true;
    error = '';
    if (password !== confirm) {
      error = "Passwords do not match";
      loading = false;
      return;
    }
    try {
      const res = await fetch('/api/users/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      if (!res.ok) {
        const data = await res.json();
        error = data.detail || 'Registration failed';
      } else {
        // handle successful registration (e.g., redirect)
        window.location.href = '/login';
      }
    } catch {
      error = 'Network error';
    }
    loading = false;
  }
</script>

<svelte:head>
  <title>Register - Zentry</title>
</svelte:head>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800">
  <form class="glass rounded-xl p-8 w-full max-w-md space-y-6 animate-fade-in-up" on:submit|preventDefault={handleRegister}>
    <h2 class="text-2xl font-bold text-white mb-2 text-center">Create your Zentry account</h2>
    {#if error}
      <div class="bg-red-500/20 text-red-300 rounded p-2 text-center">{error}</div>
    {/if}
    <div>
      <label class="block text-gray-300 mb-1">Username</label>
      <input class="w-full p-3 rounded bg-slate-700/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" bind:value={username} required />
    </div>
    <div>
      <label class="block text-gray-300 mb-1">Password</label>
      <input type="password" class="w-full p-3 rounded bg-slate-700/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" bind:value={password} required />
    </div>
    <div>
      <label class="block text-gray-300 mb-1">Confirm Password</label>
      <input type="password" class="w-full p-3 rounded bg-slate-700/60 text-white focus:outline-none focus:ring-2 focus:ring-purple-500" bind:value={confirm} required />
    </div>
    <button class="w-full btn-glow bg-gradient-to-r from-purple-500/20 to-teal-500/20 border border-purple-500/30 rounded-lg p-3 text-white font-semibold hover:bg-gradient-to-r hover:from-purple-500/30 hover:to-teal-500/30 transition-all" type="submit" disabled={loading}>
      {loading ? 'Registering...' : 'Register'}
    </button>
    <p class="text-gray-400 text-center text-sm">
      Already have an account? <a href="/login" class="text-gradient-purple-teal font-medium">Login</a>
    </p>
  </form>
</div>