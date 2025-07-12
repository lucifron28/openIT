<script lang="ts">
	import { onMount } from 'svelte';

	type User = {
		id: number;
		first_name: string;
		last_name: string;
		username: string;
		avatar?: string;
	};

	type Team = {
		id: number;
		name: string;
		description: string;
		emoji?: string;
		project_members: User[];
		owner: number;
		owner_username: string;
	};

	let teams: Team[] = [];
	let loading = false;
	let showAddTeam = false;
	let showMembersModal = false;
	let currentTeam: Team | null = null;
	let newTeam = { name: '', description: '', emoji: '' };
	let inputUserId: string = '';
	let errorMsg = '';
	let currentUserId: number | null = null;

	const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
	const API_URL = API_BASE_URL + '/api/projects/projects/';

	async function fetchCurrentUser() {
		const res = await fetch(API_BASE_URL + '/api/users/me/', { credentials: 'include' });
		if (res.ok) {
			const data = await res.json();
			currentUserId = data.id;
		}
	}

	async function fetchTeams() {
		loading = true;
		await fetchCurrentUser();
		const res = await fetch(API_URL, { credentials: 'include' });
		teams = res.ok ? await res.json() : [];
		loading = false;
	}

	async function addTeam() {
		errorMsg = '';
		const payload = {
			name: newTeam.name,
			description: newTeam.description,
			emoji: newTeam.emoji
		};
		const res = await fetch(API_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify(payload)
		});
		if (res.ok) {
			await fetchTeams();
			showAddTeam = false;
			newTeam = { name: '', description: '', emoji: '' };
		} else {
			const error = await res.json();
			errorMsg = typeof error === 'object' ? JSON.stringify(error) : error;
			alert('Failed to add team: ' + errorMsg);
		}
	}

	async function deleteTeam(teamId: number) {
		if (!confirm('Are you sure you want to delete this team?')) return;
		const res = await fetch(`${API_URL}${teamId}/`, {
			method: 'DELETE',
			credentials: 'include'
		});
		if (res.ok || res.status === 204) {
			await fetchTeams();
		} else {
			const err = await res.json();
			alert('Failed to delete: ' + JSON.stringify(err));
		}
	}

	function openMembers(team: Team) {
		currentTeam = team;
		showMembersModal = true;
	}

	async function addMember() {
		if (!inputUserId || !currentTeam) return;
		const user_id = Number(inputUserId);
		const res = await fetch(`${API_URL}${currentTeam.id}/assign_member/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify({ user_id })
		});
		if (res.ok) {
			await fetchTeams();
			inputUserId = '';
			currentTeam = teams.find(t => t.id === currentTeam?.id) || null;
		} else {
			alert('Failed to add member');
		}
	}

	async function removeMember(userId: number) {
		if (!currentTeam) return;
		const res = await fetch(`${API_URL}${currentTeam.id}/remove_member/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify({ user_id: userId })
		});
		if (res.ok) {
			await fetchTeams();
			currentTeam = teams.find(t => t.id === currentTeam?.id) || null;
		} else {
			alert('Failed to remove member');
		}
	}

	onMount(fetchTeams);
</script>

<svelte:head>
	<title>Teams - Zentry</title>
</svelte:head>

<div class="space-y-8">
	<div class="flex justify-between items-center mb-2">
		<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">Teams</h1>
		<button on:click={() => showAddTeam = true} class="bg-gradient-to-r from-purple-500 to-teal-500 text-white px-5 py-2 rounded-lg font-semibold hover:from-purple-600 hover:to-teal-600">Add Team</button>
	</div>

	{#if loading}
		<div class="text-center text-slate-400 py-8">Loading teams…</div>
	{:else if !teams.length}
		<div class="text-center text-slate-400 py-8">No teams found.</div>
	{:else}
		<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each teams as team}
				<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600 flex flex-col space-y-3">
					<div class="flex items-center gap-2">
						<span class="text-3xl">{team.emoji || '👥'}</span>
						<h2 class="text-xl font-semibold text-white">{team.name}</h2>
						{#if currentUserId === team.owner}
							<button 
								on:click={() => deleteTeam(team.id)} 
								class="ml-auto px-3 py-1 bg-red-700 text-white text-xs rounded hover:bg-red-800"
							>
								Delete
							</button>
						{/if}
					</div>
					<p class="text-slate-300">{team.description}</p>
					<div class="flex flex-wrap gap-2 mt-2">
						{#if team.project_members?.length}
							{#each team.project_members as member}
								<span class="inline-flex items-center px-2.5 py-1 rounded-lg bg-slate-700 text-white text-xs gap-1">
									<span class="text-lg">{member.avatar || '👤'}</span>
									<span>{member.first_name} {member.last_name}</span>
									{#if currentUserId === team.owner}
										<button on:click={() => removeMember(member.id)} class="ml-2 px-1 rounded hover:bg-red-700/40 text-red-300 text-xs">&times;</button>
									{/if}
								</span>
							{/each}
						{:else}
							<span class="text-slate-500 text-xs">No members</span>
						{/if}
					</div>
					<div class="flex gap-2 mt-4">
						<button on:click={() => openMembers(team)} class="bg-slate-700 hover:bg-slate-600 px-4 py-2 rounded-lg text-sm text-white">Manage Members</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

{#if showAddTeam}
	<div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50" tabindex="0" aria-modal="true" on:click={() => showAddTeam = false}>
		<div class="bg-gradient-to-br from-slate-800 to-slate-700 p-6 rounded-xl border border-slate-600 w-full max-w-md mx-4" on:click|stopPropagation>
			<h2 class="text-xl font-bold text-white mb-4">Add Team</h2>
			<form on:submit|preventDefault={addTeam} class="space-y-4">
				<div>
					<label class="block text-slate-300 mb-1">Name</label>
					<input class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white" bind:value={newTeam.name} required>
				</div>
				<div>
					<label class="block text-slate-300 mb-1">Description</label>
					<textarea class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white" rows="2" bind:value={newTeam.description}></textarea>
				</div>
				<div>
					<label class="block text-slate-300 mb-1">Emoji</label>
					<input class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white" bind:value={newTeam.emoji} maxlength="2">
				</div>
				{#if errorMsg}
					<div class="text-red-400 text-xs">{errorMsg}</div>
				{/if}
				<div class="flex justify-end gap-3">
					<button type="button" class="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg" on:click={() => showAddTeam = false}>Cancel</button>
					<button type="submit" class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg">Add</button>
				</div>
			</form>
		</div>
	</div>
{/if}

{#if showMembersModal && currentTeam}
	<div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50" tabindex="0" aria-modal="true" on:click={() => showMembersModal = false}>
		<div class="bg-gradient-to-br from-slate-800 to-slate-700 p-6 rounded-xl border border-slate-600 w-full max-w-md mx-4" on:click|stopPropagation>
			<h2 class="text-xl font-bold text-white mb-4">Manage Members for {currentTeam.name}</h2>
			{#if currentUserId === currentTeam.owner}
			<div>
				<label class="block text-slate-300 mb-1">User ID</label>
				<input
					type="number"
					class="w-full mb-4 bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white"
					bind:value={inputUserId}
					placeholder="Enter user ID to add"
					min="1"
				/>
				<button class="bg-gradient-to-r from-purple-500 to-teal-500 text-white px-4 py-2 rounded-lg" on:click={addMember} disabled={!inputUserId}>Add Member</button>
			</div>
			{/if}
			<div class="mt-6">
				<h3 class="text-slate-300 text-sm mb-2">Current Members:</h3>
				{#if currentTeam.project_members?.length}
					<ul>
						{#each currentTeam.project_members as member}
							<li class="flex items-center gap-2 text-white mb-1">
								<span class="text-lg">{member.avatar || '👤'}</span>
								<span>{member.first_name} {member.last_name} (@{member.username})</span>
							</li>
						{/each}
					</ul>
				{:else}
					<p class="text-slate-500 text-xs">No members yet</p>
				{/if}
			</div>
			<div class="flex justify-end mt-6">
				<button class="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg" on:click={() => showMembersModal = false}>Close</button>
			</div>
		</div>
	</div>
{/if}
