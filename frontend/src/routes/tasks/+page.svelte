<script lang="ts">
	import { onMount } from 'svelte';
	
	let tasks = [
		{
			id: 1,
			title: 'Set up SvelteKit frontend',
			description: 'Initialize the frontend with SvelteKit and TailwindCSS',
			status: 'completed',
			emoji: '🎨',
			priority: 'high',
			assigned_to: { username: 'alex_dev', avatar: '👨‍💻' },
			experience_reward: 50,
			created_at: '2025-06-26'
		},
		{
			id: 2,
			title: 'Design user authentication',
			description: 'Create login and registration forms',
			status: 'in_progress',
			emoji: '🔐',
			priority: 'high',
			assigned_to: { username: 'sarah_designer', avatar: '🎨' },
			experience_reward: 40,
			created_at: '2025-06-27'
		},
		{
			id: 3,
			title: 'Implement task board',
			description: 'Create drag-and-drop task board with status columns',
			status: 'todo',
			emoji: '📋',
			priority: 'medium',
			assigned_to: { username: 'mike_backend', avatar: '⚙️' },
			experience_reward: 60,
			created_at: '2025-06-28'
		},
		{
			id: 4,
			title: 'Add streak tracking',
			description: 'Implement daily streak tracking and rewards',
			status: 'todo',
			emoji: '🔥',
			priority: 'medium',
			assigned_to: { username: 'alex_dev', avatar: '👨‍💻' },
			experience_reward: 45,
			created_at: '2025-06-28'
		},
		{
			id: 5,
			title: 'Create AI coach feature',
			description: 'Implement Zenturion AI coach with suggestions',
			status: 'todo',
			emoji: '🤖',
			priority: 'low',
			assigned_to: null,
			experience_reward: 80,
			created_at: '2025-06-28'
		}
	];
	
	let showAddTask = false;
	let newTask = {
		title: '',
		description: '',
		emoji: '📝',
		priority: 'medium',
		assigned_to: null
	};
	
	// Filter tasks by status
	$: todoTasks = tasks.filter(task => task.status === 'todo');
	$: inProgressTasks = tasks.filter(task => task.status === 'in_progress');
	$: completedTasks = tasks.filter(task => task.status === 'completed');
	
	function getPriorityColor(priority: string) {
		switch (priority) {
			case 'urgent': return 'border-red-500 bg-red-500/10';
			case 'high': return 'border-orange-500 bg-orange-500/10';
			case 'medium': return 'border-yellow-500 bg-yellow-500/10';
			case 'low': return 'border-green-500 bg-green-500/10';
			default: return 'border-slate-500 bg-slate-500/10';
		}
	}
	
	function getStatusColor(status: string) {
		switch (status) {
			case 'completed': return 'bg-green-500/20 text-green-400 border-green-500/30';
			case 'in_progress': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
			case 'todo': return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
			default: return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
		}
	}
	
	function toggleTaskStatus(taskId: number) {
		const task = tasks.find(t => t.id === taskId);
		if (task) {
			if (task.status === 'todo') {
				task.status = 'in_progress';
			} else if (task.status === 'in_progress') {
				task.status = 'completed';
			} else {
				task.status = 'todo';
			}
			tasks = [...tasks]; // Trigger reactivity
		}
	}
	
	function addTask() {
		if (newTask.title.trim()) {
			const task = {
				id: Date.now(),
				...newTask,
				status: 'todo',
				experience_reward: 30,
				created_at: new Date().toISOString().split('T')[0]
			};
			tasks = [...tasks, task];
			newTask = { title: '', description: '', emoji: '📝', priority: 'medium', assigned_to: null };
			showAddTask = false;
		}
	}
</script>

<svelte:head>
	<title>Tasks - Zentry</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				Tasks Board 📋
			</h1>
			<p class="text-slate-400 mt-1">Manage your tasks and track progress</p>
		</div>
		<button 
			on:click={() => showAddTask = true}
			class="px-6 py-3 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all duration-200 flex items-center gap-2"
		>
			<span class="text-xl">➕</span>
			Add Task
		</button>
	</div>

	<!-- Task Columns -->
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
					<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-4 border border-slate-600 hover:border-slate-500 transition-colors">
						<div class="flex items-start justify-between mb-3">
							<div class="flex items-center gap-2">
								<span class="text-xl">{task.emoji}</span>
								<h3 class="font-semibold text-white">{task.title}</h3>
							</div>
							<span class="px-2 py-1 text-xs rounded-full {getPriorityColor(task.priority)} border">
								{task.priority}
							</span>
						</div>
						
						<p class="text-slate-300 text-sm mb-3">{task.description}</p>
						
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								{#if task.assigned_to}
									<span class="text-lg">{task.assigned_to.avatar}</span>
									<span class="text-sm text-slate-400">{task.assigned_to.username}</span>
								{:else}
									<span class="text-sm text-slate-400">Unassigned</span>
								{/if}
							</div>
							<div class="flex items-center gap-2">
								<span class="text-sm text-purple-400">+{task.experience_reward} XP</span>
								<button 
									on:click={() => toggleTaskStatus(task.id)}
									class="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 rounded-lg text-sm transition-colors"
								>
									Start
								</button>
							</div>
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
					<div class="bg-gradient-to-br from-blue-500/10 to-slate-700 rounded-xl p-4 border border-blue-500/30 hover:border-blue-500/50 transition-colors">
						<div class="flex items-start justify-between mb-3">
							<div class="flex items-center gap-2">
								<span class="text-xl">{task.emoji}</span>
								<h3 class="font-semibold text-white">{task.title}</h3>
							</div>
							<span class="px-2 py-1 text-xs rounded-full {getPriorityColor(task.priority)} border">
								{task.priority}
							</span>
						</div>
						
						<p class="text-slate-300 text-sm mb-3">{task.description}</p>
						
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								{#if task.assigned_to}
									<span class="text-lg">{task.assigned_to.avatar}</span>
									<span class="text-sm text-slate-400">{task.assigned_to.username}</span>
								{:else}
									<span class="text-sm text-slate-400">Unassigned</span>
								{/if}
							</div>
							<div class="flex items-center gap-2">
								<span class="text-sm text-purple-400">+{task.experience_reward} XP</span>
								<button 
									on:click={() => toggleTaskStatus(task.id)}
									class="px-3 py-1 bg-green-500/20 hover:bg-green-500/30 text-green-400 rounded-lg text-sm transition-colors"
								>
									Complete
								</button>
							</div>
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
					<div class="bg-gradient-to-br from-green-500/10 to-slate-700 rounded-xl p-4 border border-green-500/30 opacity-75">
						<div class="flex items-start justify-between mb-3">
							<div class="flex items-center gap-2">
								<span class="text-xl">{task.emoji}</span>
								<h3 class="font-semibold text-white line-through">{task.title}</h3>
							</div>
							<span class="px-2 py-1 text-xs rounded-full bg-green-500/20 text-green-400 border border-green-500/30">
								✅ Done
							</span>
						</div>
						
						<p class="text-slate-400 text-sm mb-3">{task.description}</p>
						
						<div class="flex items-center justify-between">
							<div class="flex items-center gap-2">
								{#if task.assigned_to}
									<span class="text-lg">{task.assigned_to.avatar}</span>
									<span class="text-sm text-slate-400">{task.assigned_to.username}</span>
								{:else}
									<span class="text-sm text-slate-400">Unassigned</span>
								{/if}
							</div>
							<div class="flex items-center gap-2">
								<span class="text-sm text-green-400">+{task.experience_reward} XP earned</span>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</div>

<!-- Add Task Modal -->
{#if showAddTask}
	<div
		class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
		role="dialog"
		tabindex="0"
		aria-modal="true"
		on:click={() => showAddTask = false}
		on:keydown={(e) => { if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') { showAddTask = false; } }}
	>
		<div
			class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600 w-full max-w-md mx-4"
			role="dialog"
			aria-labelledby="add-task-title"
			tabindex="-1"
			on:click|stopPropagation
			on:keydown|stopPropagation
		>
			<h2 id="add-task-title" class="text-xl font-semibold text-white mb-4">Add New Task</h2>
			
			<form on:submit|preventDefault={addTask} class="space-y-4">
				<div>
					<label for="task-title" class="block text-sm font-medium text-slate-300 mb-2">Task Title</label>
					<input 
						id="task-title"
						bind:value={newTask.title}
						type="text" 
						class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						placeholder="Enter task title..."
						required
					>
				</div>
				
				<div>
					<label for="task-desc" class="block text-sm font-medium text-slate-300 mb-2">Description</label>
					<textarea 
						id="task-desc"
						bind:value={newTask.description}
						class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						rows="3"
						placeholder="Enter task description..."
					></textarea>
				</div>
				
				<div class="grid grid-cols-2 gap-4">
					<div>
						<label for="task-emoji" class="block text-sm font-medium text-slate-300 mb-2">Emoji</label>
						<input 
							id="task-emoji"
							bind:value={newTask.emoji}
							type="text" 
							class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
							placeholder="📝"
						>
					</div>
					
					<div>
						<label for="task-priority" class="block text-sm font-medium text-slate-300 mb-2">Priority</label>
						<select 
							id="task-priority"
							bind:value={newTask.priority}
							class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
						>
							<option value="low">Low</option>
							<option value="medium">Medium</option>
							<option value="high">High</option>
							<option value="urgent">Urgent</option>
						</select>
					</div>
				</div>
				
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
