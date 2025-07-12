<script lang="ts">
	import { onMount } from 'svelte';
	
	type TeamMember = {
		id: number;
		username: string;
		first_name: string;
		last_name: string;
		avatar: string;
		role: string;
		level: number;
		experience_points: number;
		current_streak: number;
		tasks_completed: number;
		rank: number;
	};

	let teamMembers: TeamMember[] = [
		{
			id: 1,
			username: 'mike_backend',
			first_name: 'Mike',
			last_name: 'Backend',
			avatar: '⚙️',
			role: 'Backend Developer',
			level: 5,
			experience_points: 450,
			current_streak: 7,
			tasks_completed: 25,
			rank: 1
		},
		{
			id: 2,
			username: 'sarah_designer',
			first_name: 'Sarah',
			last_name: 'Designer',
			avatar: '🎨',
			role: 'UI/UX Designer',
			level: 4,
			experience_points: 320,
			current_streak: 3,
			tasks_completed: 18,
			rank: 2
		},
		{
			id: 3,
			username: 'alex_dev',
			first_name: 'Alex',
			last_name: 'Developer',
			avatar: '👨‍💻',
			role: 'Frontend Developer',
			level: 3,
			experience_points: 250,
			current_streak: 5,
			tasks_completed: 12,
			rank: 3
		},
		{
			id: 4,
			username: 'admin',
			first_name: 'Ron Vincent',
			last_name: 'Cada',
			avatar: '👑',
			role: 'Project Manager',
			level: 1,
			experience_points: 0,
			current_streak: 0,
			tasks_completed: 0,
			rank: 4
		}
	];
	
	let selectedLeaderboard = 'experience_points';
	let leaderboardTypes = [
		{ value: 'experience_points', label: 'Experience Points', emoji: '⭐' },
		{ value: 'tasks_completed', label: 'Tasks Completed', emoji: '✅' },
		{ value: 'current_streak', label: 'Current Streak', emoji: '🔥' },
		{ value: 'level', label: 'Level', emoji: '🌟' }
	];
	
	// Sort team members based on selected leaderboard
	$: sortedMembers = [...teamMembers].sort((a, b) => {
		const aValue = a[selectedLeaderboard as keyof TeamMember] as number;
		const bValue = b[selectedLeaderboard as keyof TeamMember] as number;
		return bValue - aValue;
	});
	
	function getRankColor(rank: number): string {
		switch (rank) {
			case 1: return 'bg-gradient-to-r from-yellow-400 to-yellow-600 text-yellow-900';
			case 2: return 'bg-gradient-to-r from-gray-300 to-gray-500 text-gray-900';
			case 3: return 'bg-gradient-to-r from-amber-600 to-amber-800 text-amber-100';
			default: return 'bg-slate-600 text-slate-300';
		}
	}
	
	function getRankEmoji(rank: number): string {
		switch (rank) {
			case 1: return '🥇';
			case 2: return '🥈';
			case 3: return '🥉';
			default: return `#${rank}`;
		}
	}
	
	function getLevelColor(level: number): string {
		if (level >= 5) return 'text-purple-400';
		if (level >= 3) return 'text-blue-400';
		if (level >= 1) return 'text-green-400';
		return 'text-slate-400';
	}
</script>

<svelte:head>
	<title>Team - Zentry</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				Team Leaderboard 👥
			</h1>
			<p class="text-slate-400 mt-1">See how your team is performing</p>
		</div>
		
		<!-- Leaderboard Filter -->
		<div class="flex items-center gap-2">
			<label for="leaderboard-sort" class="text-slate-400 text-sm font-medium">Sort by:</label>
			<select 
				id="leaderboard-sort"
				bind:value={selectedLeaderboard}
				class="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
			>
				{#each leaderboardTypes as type}
					<option value={type.value}>{type.emoji} {type.label}</option>
				{/each}
			</select>
		</div>
	</div>

	<!-- Team Stats Overview -->
	<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
		<div class="bg-gradient-to-br from-purple-500/20 to-teal-500/20 rounded-xl p-6 border border-purple-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-purple-200 text-sm font-medium">Total Members</p>
					<p class="text-3xl font-bold text-white">{teamMembers.length}</p>
				</div>
				<div class="text-4xl">👥</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-6 border border-green-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-green-200 text-sm font-medium">Total Tasks</p>
					<p class="text-3xl font-bold text-white">{teamMembers.reduce((sum, member) => sum + member.tasks_completed, 0)}</p>
				</div>
				<div class="text-4xl">✅</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl p-6 border border-yellow-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-yellow-200 text-sm font-medium">Average Level</p>
					<p class="text-3xl font-bold text-white">{Math.round(teamMembers.reduce((sum, member) => sum + member.level, 0) / teamMembers.length)}</p>
				</div>
				<div class="text-4xl">🌟</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-red-500/20 to-pink-500/20 rounded-xl p-6 border border-red-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-red-200 text-sm font-medium">Best Streak</p>
					<p class="text-3xl font-bold text-white">{Math.max(...teamMembers.map(member => member.current_streak))}</p>
				</div>
				<div class="text-4xl">🔥</div>
			</div>
		</div>
	</div>

	<!-- Leaderboard -->
	<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-slate-600 overflow-hidden">
		<div class="p-6 border-b border-slate-600">
			<div class="flex items-center gap-3">
				<span class="text-2xl">{leaderboardTypes.find(t => t.value === selectedLeaderboard)?.emoji}</span>
				<h2 class="text-xl font-semibold text-white">
					{leaderboardTypes.find(t => t.value === selectedLeaderboard)?.label} Leaderboard
				</h2>
			</div>
		</div>
		
		<div class="space-y-1">
			{#each sortedMembers as member, index}
				<div class="flex items-center gap-4 p-4 hover:bg-slate-700/50 transition-colors {index === 0 ? 'bg-gradient-to-r from-yellow-500/10 to-transparent' : ''}">
					<!-- Rank -->
					<div class="flex items-center justify-center w-12 h-12 rounded-full {getRankColor(index + 1)} font-bold text-lg">
						{getRankEmoji(index + 1)}
					</div>
					
					<!-- Avatar & Name -->
					<div class="flex items-center gap-3 flex-1">
						<div class="text-3xl">{member.avatar}</div>
						<div>
							<h3 class="font-semibold text-white">{member.first_name} {member.last_name}</h3>
							<p class="text-slate-400 text-sm">@{member.username}</p>
						</div>
					</div>
					
					<!-- Role -->
					<div class="hidden md:block">
						<span class="px-3 py-1 bg-slate-600 text-slate-300 rounded-full text-sm font-medium">
							{member.role}
						</span>
					</div>
					
					<!-- Level -->
					<div class="text-center">
						<div class="text-lg font-bold {getLevelColor(member.level)}">Level {member.level}</div>
						<div class="text-xs text-slate-400">{member.experience_points} XP</div>
					</div>
					
					<!-- Current Metric -->
					<div class="text-center min-w-[80px]">
						<div class="text-2xl font-bold text-white">
							{member[selectedLeaderboard as keyof TeamMember]}
						</div>
						<div class="text-xs text-slate-400">
							{selectedLeaderboard === 'experience_points' ? 'XP' : 
							 selectedLeaderboard === 'tasks_completed' ? 'tasks' :
							 selectedLeaderboard === 'current_streak' ? 'days' : 'level'}
						</div>
					</div>
					
					<!-- Streak Indicator -->
					<div class="flex items-center gap-1">
						{#if member.current_streak > 0}
							<span class="text-orange-400">🔥</span>
							<span class="text-sm text-orange-300">{member.current_streak}</span>
						{:else}
							<span class="text-slate-500">💤</span>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Team Achievements -->
	<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
		<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
			🏆 Team Achievements
		</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div class="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-lg p-4 border border-yellow-500/30">
				<div class="flex items-center gap-3">
					<span class="text-2xl">🏆</span>
					<div>
						<h3 class="font-semibold text-white">Top Performer</h3>
						<p class="text-yellow-300 text-sm">{sortedMembers[0]?.first_name} - {sortedMembers[0]?.experience_points} XP</p>
					</div>
				</div>
			</div>
			
			<div class="bg-gradient-to-br from-red-500/20 to-pink-500/20 rounded-lg p-4 border border-red-500/30">
				<div class="flex items-center gap-3">
					<span class="text-2xl">🔥</span>
					<div>
						<h3 class="font-semibold text-white">Streak Master</h3>
						<p class="text-red-300 text-sm">
							{teamMembers.reduce((max, member) => 
								member.current_streak > max.current_streak ? member : max
							).first_name} - {Math.max(...teamMembers.map(m => m.current_streak))} days
						</p>
					</div>
				</div>
			</div>
			
			<div class="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-lg p-4 border border-green-500/30">
				<div class="flex items-center gap-3">
					<span class="text-2xl">⚡</span>
					<div>
						<h3 class="font-semibold text-white">Task Champion</h3>
						<p class="text-green-300 text-sm">
							{teamMembers.reduce((max, member) => 
								member.tasks_completed > max.tasks_completed ? member : max
							).first_name} - {Math.max(...teamMembers.map(m => m.tasks_completed))} tasks
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Team Motivation -->
	<div class="bg-gradient-to-br from-purple-500/10 to-teal-500/10 rounded-xl p-6 border border-purple-500/30">
		<div class="flex items-center gap-3 mb-4">
			<div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full flex items-center justify-center text-2xl">
				🤖
			</div>
			<div>
				<h2 class="text-xl font-semibold text-white">Team Motivation</h2>
				<p class="text-slate-400 text-sm">Zenturion's team insights</p>
			</div>
		</div>
		
		<div class="bg-slate-800/50 rounded-lg p-4">
			<p class="text-slate-300 italic">
				"Great team dynamics! 🚀 Mike is crushing it with a 7-day streak - maybe he can mentor others? 
				Sarah's design work is top-notch, and Alex is making steady progress. 
				Remember to celebrate small wins together! 🎉"
			</p>
		</div>
	</div>
</div>
