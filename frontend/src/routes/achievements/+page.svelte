<script lang="ts">
	import { onMount } from 'svelte';
	
	type Badge = {
		id: number;
		name: string;
		description: string;
		emoji: string;
		experience_reward: number;
		earned: boolean;
		earned_at?: string;
		requirement_value?: number;
		current_progress?: number;
		can_claim?: boolean;
	};

	let userBadges: Badge[] = [
		{ 
			id: 1, 
			name: 'First Steps', 
			description: 'Complete your first task', 
			emoji: '🎯', 
			earned_at: '2025-06-26',
			experience_reward: 50,
			earned: true
		},
		{ 
			id: 2, 
			name: 'Dedicated', 
			description: 'Maintain a 3-day streak', 
			emoji: '🔥', 
			earned_at: '2025-06-27',
			experience_reward: 75,
			earned: true
		}
	];
	
	let availableBadges: Badge[] = [
		{ 
			id: 3, 
			name: 'Task Master', 
			description: 'Complete 10 tasks', 
			emoji: '🏆', 
			requirement_value: 10,
			current_progress: 12,
			experience_reward: 100,
			earned: true,
			can_claim: true,
			earned_at: undefined
		},
		{ 
			id: 4, 
			name: 'Streak Warrior', 
			description: 'Maintain a 7-day streak', 
			emoji: '⚡', 
			requirement_value: 7,
			current_progress: 5,
			experience_reward: 150,
			earned: false,
			can_claim: false,
			earned_at: undefined
		},
		{ 
			id: 5, 
			name: 'Level Up', 
			description: 'Reach level 5', 
			emoji: '🌟', 
			requirement_value: 5,
			current_progress: 3,
			experience_reward: 200,
			earned: false,
			can_claim: false,
			earned_at: undefined
		},
		{ 
			id: 6, 
			name: 'Elite', 
			description: 'Reach level 10', 
			emoji: '💎', 
			requirement_value: 10,
			current_progress: 3,
			experience_reward: 500,
			earned: false,
			can_claim: false,
			earned_at: undefined
		}
	];
	
	let selectedCategory = 'all';
	let categories = [
		{ value: 'all', label: 'All Badges', emoji: '🏅' },
		{ value: 'earned', label: 'Earned', emoji: '✅' },
		{ value: 'available', label: 'Available', emoji: '🎯' },
		{ value: 'locked', label: 'Locked', emoji: '🔒' }
	];
	
	// Filter badges based on selected category
	$: filteredBadges = (() => {
		const allBadges = [...userBadges, ...availableBadges];
		
		switch (selectedCategory) {
			case 'earned':
				return allBadges.filter(badge => badge.earned);
			case 'available':
				return allBadges.filter(badge => !badge.earned && 'can_claim' in badge && badge.can_claim === true);
			case 'locked':
				return allBadges.filter(badge => !badge.earned && (!('can_claim' in badge) || badge.can_claim === false));
			default:
				return allBadges;
		}
	})();
	
	function claimBadge(badgeId: number) {
		const badge = availableBadges.find(b => b.id === badgeId);
		if (badge && badge.can_claim) {
			badge.earned = true;
			badge.earned_at = new Date().toISOString().split('T')[0];
			userBadges = [...userBadges, badge];
			availableBadges = availableBadges.filter(b => b.id !== badgeId);
		}
	}
	
	function getProgressPercentage(badge: Badge): number {
		if (badge.earned) return 100;
		if (!badge.requirement_value) return 0;
		return Math.min((badge.current_progress || 0) / badge.requirement_value * 100, 100);
	}
	
	function getBadgeTypeColor(badge: Badge): string {
		if (badge.earned) return 'border-green-500 bg-green-500/10';
		if (badge.can_claim) return 'border-yellow-500 bg-yellow-500/10 animate-pulse';
		return 'border-slate-500 bg-slate-500/5';
	}
</script>

<svelte:head>
	<title>Achievements - AQuest</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				Achievements 🏆
			</h1>
			<p class="text-slate-400 mt-1">Track your progress and earn badges</p>
		</div>
		
		<!-- Category Filter -->
		<div class="flex items-center gap-2">
			<label for="category-filter" class="text-slate-400 text-sm font-medium">Filter:</label>
			<select 
				id="category-filter"
				bind:value={selectedCategory}
				class="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:border-purple-500 focus:outline-none"
			>
				{#each categories as category}
					<option value={category.value}>{category.emoji} {category.label}</option>
				{/each}
			</select>
		</div>
	</div>

	<!-- Achievement Stats -->
	<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
		<div class="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-xl p-6 border border-green-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-green-200 text-sm font-medium">Badges Earned</p>
					<p class="text-3xl font-bold text-white">{userBadges.length}</p>
				</div>
				<div class="text-4xl">🏅</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl p-6 border border-yellow-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-yellow-200 text-sm font-medium">Ready to Claim</p>
					<p class="text-3xl font-bold text-white">{availableBadges.filter(b => b.can_claim).length}</p>
				</div>
				<div class="text-4xl">🎁</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-xl p-6 border border-purple-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-purple-200 text-sm font-medium">Total XP from Badges</p>
					<p class="text-3xl font-bold text-white">{userBadges.reduce((sum, badge) => sum + badge.experience_reward, 0)}</p>
				</div>
				<div class="text-4xl">⭐</div>
			</div>
		</div>
		
		<div class="bg-gradient-to-br from-blue-500/20 to-teal-500/20 rounded-xl p-6 border border-blue-500/30">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-blue-200 text-sm font-medium">Completion Rate</p>
					<p class="text-3xl font-bold text-white">{Math.round((userBadges.length / (userBadges.length + availableBadges.length)) * 100)}%</p>
				</div>
				<div class="text-4xl">📊</div>
			</div>
		</div>
	</div>

	<!-- Badges Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
		{#each filteredBadges as badge}
			<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border {getBadgeTypeColor(badge)} relative overflow-hidden">
				<!-- Earned Badge Glow Effect -->
				{#if badge.earned}
					<div class="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-500/5 pointer-events-none"></div>
				{/if}
				
				<!-- Claimable Badge Animation -->
				{#if badge.can_claim && !badge.earned}
					<div class="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-orange-500/5 pointer-events-none animate-pulse"></div>
				{/if}
				
				<div class="relative z-10">
					<!-- Badge Header -->
					<div class="flex items-start justify-between mb-4">
						<div class="flex items-center gap-3">
							<span class="text-4xl">{badge.emoji}</span>
							<div>
								<h3 class="font-semibold text-white">{badge.name}</h3>
								{#if badge.earned}
									<span class="text-xs text-green-400 flex items-center gap-1">
										✅ Earned {badge.earned_at}
									</span>
								{:else if badge.can_claim}
									<span class="text-xs text-yellow-400 flex items-center gap-1 animate-pulse">
										🎁 Ready to claim!
									</span>
								{:else}
									<span class="text-xs text-slate-400">
										🔒 Locked
									</span>
								{/if}
							</div>
						</div>
						
						{#if badge.earned}
							<div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white text-sm">
								✓
							</div>
						{:else if badge.can_claim}
							<button 
								on:click={() => claimBadge(badge.id)}
								class="px-3 py-1 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-lg text-sm font-medium hover:from-yellow-600 hover:to-orange-600 transition-all animate-pulse"
							>
								Claim
							</button>
						{/if}
					</div>
					
					<!-- Badge Description -->
					<p class="text-slate-300 text-sm mb-4">{badge.description}</p>
					
					<!-- Progress Bar (for non-earned badges) -->
					{#if !badge.earned && badge.requirement_value}
						<div class="space-y-2">
							<div class="flex justify-between text-sm">
								<span class="text-slate-400">Progress</span>
								<span class="text-slate-300">
									{badge.current_progress}/{badge.requirement_value}
								</span>
							</div>
							<div class="w-full bg-slate-700 rounded-full h-2">
								<div 
									class="h-2 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full transition-all duration-700"
									style="width: {getProgressPercentage(badge)}%"
								></div>
							</div>
						</div>
					{/if}
					
					<!-- Reward -->
					<div class="flex items-center justify-between mt-4 pt-4 border-t border-slate-600">
						<span class="text-slate-400 text-sm">Reward</span>
						<span class="text-purple-400 font-bold">+{badge.experience_reward} XP</span>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<!-- Achievement Categories -->
	<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
		<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
			🎯 Achievement Categories
		</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
			<div class="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-lg p-4 border border-green-500/30">
				<div class="flex items-center gap-3 mb-2">
					<span class="text-2xl">📝</span>
					<h3 class="font-semibold text-white">Task Badges</h3>
				</div>
				<p class="text-green-300 text-sm">Complete tasks to earn these badges</p>
				<div class="mt-2">
					<span class="text-xs text-slate-400">
						{[...userBadges, ...availableBadges].filter(b => b.description.includes('task')).length} available
					</span>
				</div>
			</div>
			
			<div class="bg-gradient-to-br from-red-500/20 to-pink-500/20 rounded-lg p-4 border border-red-500/30">
				<div class="flex items-center gap-3 mb-2">
					<span class="text-2xl">🔥</span>
					<h3 class="font-semibold text-white">Streak Badges</h3>
				</div>
				<p class="text-red-300 text-sm">Maintain daily streaks for rewards</p>
				<div class="mt-2">
					<span class="text-xs text-slate-400">
						{[...userBadges, ...availableBadges].filter(b => b.description.includes('streak')).length} available
					</span>
				</div>
			</div>
			
			<div class="bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-lg p-4 border border-purple-500/30">
				<div class="flex items-center gap-3 mb-2">
					<span class="text-2xl">🌟</span>
					<h3 class="font-semibold text-white">Level Badges</h3>
				</div>
				<p class="text-purple-300 text-sm">Level up to unlock these achievements</p>
				<div class="mt-2">
					<span class="text-xs text-slate-400">
						{[...userBadges, ...availableBadges].filter(b => b.description.includes('level')).length} available
					</span>
				</div>
			</div>
			
			<div class="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-lg p-4 border border-yellow-500/30">
				<div class="flex items-center gap-3 mb-2">
					<span class="text-2xl">🎉</span>
					<h3 class="font-semibold text-white">Special Badges</h3>
				</div>
				<p class="text-yellow-300 text-sm">Rare achievements for special milestones</p>
				<div class="mt-2">
					<span class="text-xs text-slate-400">Coming soon!</span>
				</div>
			</div>
		</div>
	</div>
</div>
