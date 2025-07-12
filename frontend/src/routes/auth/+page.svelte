<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	
	let email = '';
	let password = '';
	let username = '';
	let confirmPassword = '';
	let isLogin = true;
	let loading = false;
	let error = '';

	async function handleSubmit() {
		loading = true;
		error = '';
		
		try {
			if (isLogin) {
				const result = await auth.login(email, password);
				if (result.success) {
					goto('/');
				} else {
					error = result.error || 'Login failed';
				}
			} else {
				const result = await auth.register(email, username, password, confirmPassword);
				if (result.success) {
					// Switch to login mode after successful registration
					isLogin = true;
					error = '';
					// Clear form
					password = '';
					confirmPassword = '';
				} else {
					if (typeof result.error === 'object') {
						error = Object.values(result.error).flat().join(', ');
					} else {
						error = result.error || 'Registration failed';
					}
				}
			}
		} catch (err) {
			error = 'An unexpected error occurred';
		}
		
		loading = false;
	}

	function toggleMode() {
		isLogin = !isLogin;
		error = '';
		password = '';
		confirmPassword = '';
	}
</script>

<svelte:head>
	<title>{isLogin ? 'Login' : 'Register'} - Zentry</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
	<div class="max-w-md w-full">
		<!-- Logo -->
		<div class="text-center mb-8">
			<div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
				<span class="text-white font-bold text-2xl">Z</span>
			</div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				{isLogin ? 'Welcome Back' : 'Join Zentry'}
			</h1>
			<p class="text-slate-400 mt-2">
				{isLogin ? 'Sign in to continue your journey' : 'Start leveling up your productivity'}
			</p>
		</div>

		<!-- Auth Form -->
		<div class="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-8 border border-slate-700/50">
			<form on:submit|preventDefault={handleSubmit} class="space-y-6">
				<!-- Email -->
				<div>
					<label for="email" class="block text-sm font-medium text-slate-300 mb-2">
						Email Address
					</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						required
						class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-purple-500 focus:outline-none transition-colors"
						placeholder="Enter your email"
					/>
				</div>

				<!-- Username (Register only) -->
				{#if !isLogin}
					<div>
						<label for="username" class="block text-sm font-medium text-slate-300 mb-2">
							Username
						</label>
						<input
							id="username"
							type="text"
							bind:value={username}
							required
							class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-purple-500 focus:outline-none transition-colors"
							placeholder="Choose a username"
						/>
					</div>
				{/if}

				<!-- Password -->
				<div>
					<label for="password" class="block text-sm font-medium text-slate-300 mb-2">
						Password
					</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						required
						class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-purple-500 focus:outline-none transition-colors"
						placeholder="Enter your password"
					/>
				</div>

				<!-- Confirm Password (Register only) -->
				{#if !isLogin}
					<div>
						<label for="confirmPassword" class="block text-sm font-medium text-slate-300 mb-2">
							Confirm Password
						</label>
						<input
							id="confirmPassword"
							type="password"
							bind:value={confirmPassword}
							required
							class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:border-purple-500 focus:outline-none transition-colors"
							placeholder="Confirm your password"
						/>
					</div>
				{/if}

				<!-- Error Message -->
				{#if error}
					<div class="bg-red-500/20 border border-red-500/30 rounded-lg p-3">
						<p class="text-red-400 text-sm">{error}</p>
					</div>
				{/if}

				<!-- Submit Button -->
				<button
					type="submit"
					disabled={loading}
					class="w-full py-3 bg-gradient-to-r from-purple-500 to-teal-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all transform hover:scale-105 disabled:opacity-50 disabled:transform-none"
				>
					{#if loading}
						<div class="flex items-center justify-center">
							<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
							{isLogin ? 'Signing In...' : 'Creating Account...'}
						</div>
					{:else}
						{isLogin ? 'Sign In' : 'Create Account'}
					{/if}
				</button>
			</form>

			<!-- Toggle Mode -->
			<div class="mt-6 text-center">
				<p class="text-slate-400">
					{isLogin ? "Don't have an account?" : 'Already have an account?'}
					<button
						type="button"
						on:click={toggleMode}
						class="text-purple-400 hover:text-purple-300 font-medium ml-1 transition-colors"
					>
						{isLogin ? 'Sign up' : 'Sign in'}
					</button>
				</p>
			</div>
		</div>
	</div>
</div>
