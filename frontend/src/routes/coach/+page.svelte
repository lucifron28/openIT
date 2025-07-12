<script lang="ts">
	import { onMount } from 'svelte';
	
	let messages = [
		{
			id: 1,
			type: 'ai',
			content: "Hello! I'm Zenturion, your AI productivity coach! 🤖 I'm here to help you stay motivated and achieve your goals. How can I assist you today?",
			timestamp: new Date(Date.now() - 300000) // 5 minutes ago
		}
	];
	
	let currentMessage = '';
	let isTyping = false;
	
	let suggestedPrompts = [
		{
			icon: '📊',
			title: 'Suggest a 2-week sprint',
			prompt: 'Can you help me plan a 2-week sprint for my team? We have 5 developers and need to prioritize our tasks.'
		},
		{
			icon: '🚀',
			title: 'Motivate the team',
			prompt: 'Our team morale seems low lately. Can you give us some motivational advice and team building ideas?'
		},
		{
			icon: '📈',
			title: 'Analyze productivity',
			prompt: 'Can you analyze my productivity patterns and suggest improvements based on my task completion history?'
		},
		{
			icon: '⚡',
			title: 'Quick task suggestions',
			prompt: 'I have 30 minutes free. What quick tasks can I complete to maintain my streak?'
		},
		{
			icon: '🎯',
			title: 'Set goals',
			prompt: 'Help me set realistic goals for the next month based on my current performance.'
		},
		{
			icon: '🔥',
			title: 'Maintain streak',
			prompt: 'I\'m worried about breaking my streak. What can I do to stay consistent?'
		}
	];
	
	let insights = [
		{
			type: 'streak',
			icon: '🔥',
			title: 'Streak Reminder',
			message: 'You\'re on a 5-day streak! Complete one more task today to keep it going.',
			priority: 'high'
		},
		{
			type: 'team',
			icon: '👥',
			title: 'Team Check-in',
			message: 'Sarah from UI/UX hasn\'t been active lately. Maybe check in with her?',
			priority: 'medium'
		},
		{
			type: 'productivity',
			icon: '📊',
			title: 'Productivity Tip',
			message: 'You\'re most productive in the morning. Try scheduling complex tasks between 9-11 AM.',
			priority: 'low'
		},
		{
			type: 'achievement',
			icon: '🏆',
			title: 'Achievement Available',
			message: 'You\'re close to earning the "Task Master" badge! Complete 3 more tasks.',
			priority: 'medium'
		}
	];
	
	function sendMessage() {
		if (!currentMessage.trim()) return;
		
		// Add user message
		messages = [...messages, {
			id: Date.now(),
			type: 'user',
			content: currentMessage,
			timestamp: new Date()
		}];
		
		const userMsg = currentMessage;
		currentMessage = '';
		isTyping = true;
		
		// Simulate AI response
		setTimeout(() => {
			const aiResponse = generateAIResponse(userMsg);
			messages = [...messages, {
				id: Date.now(),
				type: 'ai',
				content: aiResponse,
				timestamp: new Date()
			}];
			isTyping = false;
		}, 1500);
	}
	
	function useSuggestedPrompt(prompt: string) {
		currentMessage = prompt;
		sendMessage();
	}
	
	function generateAIResponse(userMessage: string) {
		const responses = [
			"Great question! Based on your current progress, I'd recommend focusing on high-priority tasks that align with your team's goals. Let me break this down for you... 🎯",
			"I've analyzed your productivity patterns, and here's what I found: You tend to be most effective when you tackle challenging tasks early in the day. Consider blocking your calendar for deep work! 📊",
			"That's an excellent goal! To maintain your momentum, I suggest setting micro-milestones. Small wins lead to big achievements! 🚀",
			"I notice you're doing fantastic with consistency! Your streak shows real dedication. To keep it up, try the 2-minute rule: if a task takes less than 2 minutes, do it now! ⚡",
			"Team collaboration is key to success! I recommend scheduling regular check-ins and celebrating small wins together. Recognition boosts morale! 👥"
		];
		
		return responses[Math.floor(Math.random() * responses.length)];
	}
	
	function formatTime(timestamp: Date) {
		const now = new Date();
		const diff = now.getTime() - timestamp.getTime();
		const minutes = Math.floor(diff / 60000);
		
		if (minutes < 1) return 'Just now';
		if (minutes < 60) return `${minutes}m ago`;
		
		const hours = Math.floor(minutes / 60);
		if (hours < 24) return `${hours}h ago`;
		
		const days = Math.floor(hours / 24);
		return `${days}d ago`;
	}
	
	function getPriorityColor(priority: string) {
		switch (priority) {
			case 'high': return 'border-red-500 bg-red-500/10';
			case 'medium': return 'border-yellow-500 bg-yellow-500/10';
			case 'low': return 'border-green-500 bg-green-500/10';
			default: return 'border-slate-500 bg-slate-500/10';
		}
	}
</script>

<svelte:head>
	<title>AI Coach - Zenturion - Zentry</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				AI Coach - Zenturion 🤖
			</h1>
			<p class="text-slate-400 mt-1">Your personal productivity assistant</p>
		</div>
		
		<div class="flex items-center gap-2">
			<div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
			<span class="text-green-400 text-sm font-medium">Online</span>
		</div>
	</div>

	<!-- AI Insights -->
	<div class="bg-gradient-to-br from-purple-500/10 to-teal-500/10 rounded-xl p-6 border border-purple-500/30">
		<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
			💡 Current Insights
		</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			{#each insights as insight}
				<div class="bg-slate-800/50 rounded-lg p-4 border {getPriorityColor(insight.priority)}">
					<div class="flex items-start gap-3">
						<span class="text-2xl">{insight.icon}</span>
						<div class="flex-1">
							<h3 class="font-semibold text-white mb-1">{insight.title}</h3>
							<p class="text-slate-300 text-sm">{insight.message}</p>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>

	<!-- Chat Interface -->
	<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
		<!-- Chat Messages -->
		<div class="lg:col-span-2 bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-slate-600 flex flex-col h-[600px]">
			<!-- Chat Header -->
			<div class="p-4 border-b border-slate-600">
				<div class="flex items-center gap-3">
					<div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full flex items-center justify-center text-xl">
						🤖
					</div>
					<div>
						<h3 class="font-semibold text-white">Zenturion</h3>
						<p class="text-slate-400 text-sm">AI Productivity Coach</p>
					</div>
				</div>
			</div>
			
			<!-- Messages -->
			<div class="flex-1 overflow-y-auto p-4 space-y-4">
				{#each messages as message}
					<div class="flex {message.type === 'user' ? 'justify-end' : 'justify-start'}">
						<div class="max-w-[80%] {message.type === 'user' 
							? 'bg-gradient-to-r from-purple-500 to-teal-500' 
							: 'bg-slate-700'} rounded-2xl p-4">
							<p class="text-white text-sm">{message.content}</p>
							<p class="text-xs {message.type === 'user' ? 'text-purple-100' : 'text-slate-400'} mt-2">
								{formatTime(message.timestamp)}
							</p>
						</div>
					</div>
				{/each}
				
				{#if isTyping}
					<div class="flex justify-start">
						<div class="bg-slate-700 rounded-2xl p-4">
							<div class="flex items-center gap-2">
								<div class="flex gap-1">
									<div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
									<div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
									<div class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
								</div>
								<span class="text-slate-400 text-sm">Zenturion is typing...</span>
							</div>
						</div>
					</div>
				{/if}
			</div>
			
			<!-- Message Input -->
			<div class="p-4 border-t border-slate-600">
				<form on:submit|preventDefault={sendMessage} class="flex gap-2">
					<input 
						bind:value={currentMessage}
						type="text" 
						class="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white focus:border-purple-500 focus:outline-none"
						placeholder="Ask Zenturion anything..."
						disabled={isTyping}
					>
					<button 
						type="submit"
						disabled={!currentMessage.trim() || isTyping}
						class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg hover:from-purple-600 hover:to-teal-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
					>
						<span class="text-lg">📤</span>
					</button>
				</form>
			</div>
		</div>

		<!-- Suggested Prompts -->
		<div class="space-y-6">
			<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
				<h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
					💡 Suggested Prompts
				</h3>
				
				<div class="space-y-3">
					{#each suggestedPrompts as suggestion}
						<button 
							on:click={() => useSuggestedPrompt(suggestion.prompt)}
							class="w-full text-left p-3 bg-slate-700/50 hover:bg-slate-700 rounded-lg border border-slate-600 hover:border-slate-500 transition-colors"
							disabled={isTyping}
						>
							<div class="flex items-center gap-3">
								<span class="text-xl">{suggestion.icon}</span>
								<div>
									<h4 class="font-medium text-white text-sm">{suggestion.title}</h4>
									<p class="text-slate-400 text-xs line-clamp-2">{suggestion.prompt}</p>
								</div>
							</div>
						</button>
					{/each}
				</div>
			</div>

			<!-- AI Stats -->
			<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
				<h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
					📊 AI Analytics
				</h3>
				
				<div class="space-y-4">
					<div class="flex items-center justify-between">
						<span class="text-slate-400 text-sm">Conversations</span>
						<span class="text-white font-bold">{messages.length}</span>
					</div>
					
					<div class="flex items-center justify-between">
						<span class="text-slate-400 text-sm">Insights Generated</span>
						<span class="text-white font-bold">{insights.length}</span>
					</div>
					
					<div class="flex items-center justify-between">
						<span class="text-slate-400 text-sm">Success Rate</span>
						<span class="text-green-400 font-bold">95%</span>
					</div>
					
					<div class="pt-3 border-t border-slate-600">
						<div class="flex items-center gap-2 text-sm text-slate-400">
							<span class="w-2 h-2 bg-green-500 rounded-full"></span>
							Last updated: Just now
						</div>
					</div>
				</div>
			</div>

			<!-- Quick Actions -->
			<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
				<h3 class="text-lg font-semibold text-white mb-4 flex items-center gap-2">
					⚡ Quick Actions
				</h3>
				
				<div class="space-y-2">
					<button class="w-full p-3 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg text-sm transition-colors flex items-center gap-2">
						<span>🎯</span>
						Review Goals
					</button>
					
					<button class="w-full p-3 bg-teal-500/20 hover:bg-teal-500/30 text-teal-300 rounded-lg text-sm transition-colors flex items-center gap-2">
						<span>📈</span>
						Track Progress
					</button>
					
					<button class="w-full p-3 bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 rounded-lg text-sm transition-colors flex items-center gap-2">
						<span>🔔</span>
						Set Reminders
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
