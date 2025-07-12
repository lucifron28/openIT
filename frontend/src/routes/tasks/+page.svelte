<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { get } from 'svelte/store';

	const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
	let project: any = null;
	let currentUser: any = null;
	let tasks: any[] = [];
	let projects: any[] = [];
	let loading = true;
	let errorMsg = '';
	let selectedProject: string = '';

	let showAddTask = false;
	let newTask = {
		name: '',
		description: '',
		emoji: '📝',
		priority: 'medium',
		project: ''
	};

	let projectId: number | null = null;
	$: {
		const paramsId = get(page).params.projectId;
		projectId = paramsId ? Number(paramsId) : null;
	}

	onMount(() => { loadAll(); });
	$: if (projectId !== undefined) { loadAll(); }

	async function fetchCurrentUser() {
		const res = await fetch(`${API_BASE_URL}/api/users/me/`, { credentials: 'include' });
		if (res.ok) currentUser = await res.json();
		else currentUser = null;
	}
	async function fetchProjects() {
		const res = await fetch(`${API_BASE_URL}/api/projects/projects/`, { credentials: 'include' });
		projects = res.ok ? await res.json() : [];
	}
	async function fetchProject() {
		project = null;
		if (!projectId) return;
		const res = await fetch(`${API_BASE_URL}/api/projects/projects/${projectId}/`, { credentials: 'include' });
		if (res.ok) {
			project = await res.json();
		}
	}
	async function fetchTasks() {
		tasks = [];
		loading = true;
		if (project && projectId) {
			const res = await fetch(`${API_BASE_URL}/api/projects/projects/${projectId}/tasks/`, { credentials: 'include' });
			tasks = res.ok ? await res.json() : [];
		} else {
			const res = await fetch(`${API_BASE_URL}/api/projects/tasks/`, { credentials: 'include' });
			tasks = res.ok ? await res.json() : [];
		}
		loading = false;
	}

	async function loadAll() {
		loading = true;
		errorMsg = '';
		await fetchCurrentUser();
		await fetchProjects();
		await fetchProject();
		await fetchTasks();
		loading = false;
	}

	$: filteredTasks = selectedProject
		? tasks.filter(task => (task.project && `${task.project}` === `${selectedProject}`))
		: tasks;

	$: todoTasks = filteredTasks.filter(task => task.status === 'todo');
	$: inProgressTasks = filteredTasks.filter(task => task.status === 'in_progress');
	$: completedTasks = filteredTasks.filter(task => task.status === 'completed');

	function getPriorityColor(priority: string) {
		switch (priority) {
			case 'urgent': return 'border-red-500 bg-red-500/10';
			case 'high': return 'border-orange-500 bg-orange-500/10';
			case 'medium': return 'border-yellow-500 bg-yellow-500/10';
			case 'low': return 'border-green-500 bg-green-500/10';
			default: return 'border-slate-500 bg-slate-500/10';
		}
	}

	function getProjectName(projectId: number | string) {
		const p = projects.find(p => `${p.id}` === `${projectId}`);
		return p ? p.name : '—';
	}

	function canEditTask(task: any) {
		const assignedId = typeof task.assigned_to === 'object' ? task.assigned_to?.id : task.assigned_to;
		const createdId = typeof task.created_by === 'object' ? task.created_by?.id : task.created_by;
		const projectOwnerId = typeof project?.owner === 'object' ? project?.owner?.id : project?.owner;
		return (
			!assignedId ||
			assignedId === currentUser?.id ||
			createdId === currentUser?.id ||
			projectOwnerId === currentUser?.id
		);
	}

	async function toggleTaskStatus(task: any) {
		let newStatus = task.status === 'todo' ? 'in_progress'
			: task.status === 'in_progress' ? 'completed' : 'todo';
		let body: any = { status: newStatus };
		if (!task.assigned_to) {
			body.assigned_to = currentUser.id;
		}
		const res = await fetch(`${API_BASE_URL}/api/projects/tasks/${task.id}/`, {
			method: 'PATCH',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify(body)
		});
		if (res.ok) await fetchTasks();
	}

	async function deleteTask(task: any) {
		if (!canEditTask(task)) return;
		if (!confirm('Are you sure you want to delete this task?')) return;
		const url = `${API_BASE_URL}/api/projects/tasks/${task.id}/`;
		const res = await fetch(url, {
			method: 'DELETE',
			credentials: 'include'
		});
		if (res.ok) {
			await fetchTasks();
		} else {
			const err = await res.json();
			errorMsg = typeof err === 'object' ? JSON.stringify(err) : err;
		}
	}

	async function addTask() {
		errorMsg = '';
		if (!newTask.name.trim()) {
			errorMsg = 'Task title required.';
			return;
		}
		let payload: any = {
			name: newTask.name,
			description: newTask.description,
			emoji: newTask.emoji,
			priority: newTask.priority,
			status: 'todo',
			project: projectId || newTask.project || null
		};
		let url: string;
		if (project && projectId) {
			url = `${API_BASE_URL}/api/projects/projects/${projectId}/tasks/`;
		} else {
			url = `${API_BASE_URL}/api/projects/tasks/`;
		}
		const res = await fetch(url, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			credentials: 'include',
			body: JSON.stringify(payload)
		});
		if (res.ok) {
			await fetchTasks();
			showAddTask = false;
			newTask = { name: '', description: '', emoji: '📝', priority: 'medium', project: '' };
		} else {
			const err = await res.json();
			errorMsg = typeof err === 'object' ? JSON.stringify(err) : err;
		}
	}
</script>

<svelte:head>
	<title>Tasks - AQuest</title>
</svelte:head>

<div class="space-y-6">
	<div class="flex items-center justify-between flex-wrap gap-3">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				Tasks Board 📋
			</h1>
			{#if project}
				<p class="text-slate-400 mt-1">Project: <span class="font-semibold">{project.name}</span></p>
			{:else}
				<p class="text-slate-400 mt-1">No project selected. Tasks here are global or personal.</p>
			{/if}
		</div>
		<div class="flex items-center gap-3">
			{#if !project && projects.length > 0}
				<select bind:value={selectedProject} class="bg-slate-700 text-white rounded-lg px-3 py-2 border border-slate-600 focus:border-purple-500">
					<option value="">All Projects</option>
					{#each projects as p}
						<option value={p.id}>{p.name}</option>
					{/each}
				</select>
			{/if}
			{#if currentUser}
				<button 
					on:click={() => showAddTask = true}
					class="px-6 py-3 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all duration-200 flex items-center gap-2"
				>
					<span class="text-xl">➕</span>
					Add Task
				</button>
			{/if}
		</div>
	</div>

	{#if loading}
		<div class="text-center text-slate-400 py-8">Loading tasks…</div>
	{:else}
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- To Do Column -->
		<div class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-xl font-semibold text-white flex items-center gap-2">
					<span class="w-3 h-3 bg-slate-500 rounded-full"></span>
					To Do
				</h2>
				<span class="px-3 py-1 bg-slate-500/20 text-slate-400 rounded-full text-sm">
					{todoTasks.length}
				</span>
			</div>
			<div class="space-y-3">
				{#each todoTasks as task}
					<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 border border-slate-600 hover:border-slate-500 transition-colors min-h-[170px] flex flex-col justify-between">
						<div>
							<div class="flex items-center justify-between gap-2 mb-2">
								<div class="flex items-center gap-2 min-w-0">
									<span class="text-xl flex-shrink-0">{task.emoji}</span>
									<h3 class="font-semibold text-white text-base truncate">{task.name}</h3>
								</div>
								<span class="px-2 py-1 text-xs rounded-full {getPriorityColor(task.priority)} border whitespace-nowrap">
									{task.priority}
								</span>
							</div>
							<p class="text-slate-300 text-sm mb-3 break-words">{task.description}</p>
						</div>
						<div class="flex items-center justify-between gap-2 flex-wrap">
							<div class="flex items-center gap-2">
								<span class="text-sm text-slate-400">
									Assigned project: 
									{#if task.project}
										{getProjectName(task.project)}
									{:else}
										None
									{/if}
								</span>
							</div>
							{#if canEditTask(task)}
							<div class="flex items-center gap-2 flex-wrap">
								<span class="text-sm text-purple-400 whitespace-nowrap">+{task.experience_reward} XP</span>
								<button 
									on:click={() => toggleTaskStatus(task)}
									class="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg text-sm transition-colors whitespace-nowrap"
								>
									Start
								</button>
								<button
									on:click={() => deleteTask(task)}
									class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm transition-colors whitespace-nowrap"
								>
									Delete
								</button>
							</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
		<!-- In Progress Column -->
		<div class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-xl font-semibold text-white flex items-center gap-2">
					<span class="w-3 h-3 bg-blue-500 rounded-full"></span>
					In Progress
				</h2>
				<span class="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-sm">
					{inProgressTasks.length}
				</span>
			</div>
			<div class="space-y-3">
				{#each inProgressTasks as task}
					<div class="bg-gradient-to-br from-blue-500/10 to-slate-700 rounded-xl p-4 border border-blue-500/30 hover:border-blue-500/50 transition-colors min-h-[170px] flex flex-col justify-between">
						<div>
							<div class="flex items-center justify-between gap-2 mb-2">
								<div class="flex items-center gap-2 min-w-0">
									<span class="text-xl flex-shrink-0">{task.emoji}</span>
									<h3 class="font-semibold text-white text-base truncate">{task.name}</h3>
								</div>
								<span class="px-2 py-1 text-xs rounded-full {getPriorityColor(task.priority)} border whitespace-nowrap">
									{task.priority}
								</span>
							</div>
							<p class="text-slate-300 text-sm mb-3 break-words">{task.description}</p>
						</div>
						<div class="flex items-center justify-between gap-2 flex-wrap">
							<div class="flex items-center gap-2">
								<span class="text-sm text-slate-400">
									Assigned project: 
									{#if task.project}
										{getProjectName(task.project)}
									{:else}
										None
									{/if}
								</span>
							</div>
							{#if canEditTask(task)}
							<div class="flex items-center gap-2 flex-wrap">
								<span class="text-sm text-purple-400 whitespace-nowrap">+{task.experience_reward} XP</span>
								<button 
									on:click={() => toggleTaskStatus(task)}
									class="px-3 py-1 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-lg text-sm transition-colors whitespace-nowrap"
								>
									Complete
								</button>
								<button
									on:click={() => deleteTask(task)}
									class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm transition-colors whitespace-nowrap"
								>
									Delete
								</button>
							</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
		<!-- Completed Column -->
		<div class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-xl font-semibold text-white flex items-center gap-2">
					<span class="w-3 h-3 bg-green-500 rounded-full"></span>
					Completed
				</h2>
				<span class="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
					{completedTasks.length}
				</span>
			</div>
			<div class="space-y-3">
				{#each completedTasks as task}
					<div class="bg-gradient-to-br from-green-500/10 to-slate-700 rounded-xl p-4 border border-green-500/30 opacity-80 flex flex-col justify-between min-h-[170px]">
						<div>
							<div class="flex items-center justify-between gap-2 mb-2">
								<div class="flex items-center gap-2 min-w-0">
									<span class="text-xl flex-shrink-0">{task.emoji}</span>
									<h3 class="font-semibold text-white text-base line-through truncate">{task.name}</h3>
								</div>
								<span class="px-2 py-1 text-xs rounded-full bg-green-500/20 text-green-400 border border-green-500/30 whitespace-nowrap">
									✅ Done
								</span>
							</div>
							<p class="text-slate-400 text-sm mb-3 break-words">{task.description}</p>
						</div>
						<div class="flex items-center justify-between gap-2 flex-wrap">
							<div class="flex items-center gap-2">
								<span class="text-sm text-slate-400">
									Assigned project: 
									{#if task.project}
										{getProjectName(task.project)}
									{:else}
										None
									{/if}
								</span>
							</div>
							{#if canEditTask(task)}
							<div class="flex items-center gap-2 flex-wrap">
								<span class="text-sm text-green-400 whitespace-nowrap">+{task.experience_reward} XP earned</span>
								<button
									on:click={() => deleteTask(task)}
									class="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm transition-colors whitespace-nowrap"
								>
									Delete
								</button>
							</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
	{/if}
</div>

{#if showAddTask}
	<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50" role="dialog" tabindex="0" aria-modal="true" on:click={() => showAddTask = false}>
		<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600 w-full max-w-md mx-4" on:click|stopPropagation>
			<h2 class="text-xl font-semibold text-white mb-4">Add New Task</h2>
			<form on:submit|preventDefault={addTask} class="space-y-4">
				<div>
					<label class="block text-sm font-medium text-slate-300 mb-2">Task Title</label>
					<input 
						bind:value={newTask.name}
						type="text" 
						class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						placeholder="Enter task title..."
						required
					>
				</div>
				<div>
					<label class="block text-sm font-medium text-slate-300 mb-2">Description</label>
					<textarea 
						bind:value={newTask.description}
						class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						rows="3"
						placeholder="Enter task description..."
					></textarea>
				</div>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium text-slate-300 mb-2">Emoji</label>
						<input 
							bind:value={newTask.emoji}
							type="text" 
							class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
							placeholder="📝"
						>
					</div>
					<div>
						<label class="block text-sm font-medium text-slate-300 mb-2">Priority</label>
						<select 
							bind:value={newTask.priority}
							class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						>
							<option value="low">Low</option>
							<option value="medium">Medium</option>
							<option value="high">High</option>
							<option value="urgent">Urgent</option>
						</select>
					</div>
					{#if !project}
					<div class="col-span-2">
						<label class="block text-sm font-medium text-slate-300 mb-2">Assign to Project</label>
						<select bind:value={newTask.project} class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white">
							<option value="">None (global/personal task)</option>
							{#each projects as p}
								<option value={p.id}>{p.name}</option>
							{/each}
						</select>
					</div>
					{/if}
				</div>
				{#if errorMsg}
					<div class="text-red-400 text-xs">{errorMsg}</div>
				{/if}
				<div class="flex justify-end gap-3 pt-4">
					<button 
						type="button"
						on:click={() => showAddTask = false}
						class="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg transition-colors"
					>
						Cancel
					</button>
					<button 
						type="submit"
						class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all"
					>
						Add Task
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}
