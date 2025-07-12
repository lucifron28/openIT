// AI Service for Zenturion Coach
export const ai = {
	// Placeholder API key - in production, this should be set via environment variables
	API_KEY: import.meta.env.VITE_OPENAI_API_KEY || '',
	API_URL: 'https://api.openai.com/v1/chat/completions',

	async generateResponse(userMessage: string, conversationHistory: any[] = []): Promise<string> {
		// If no API key is set, return fallback responses
		if (this.API_KEY === 'your-openai-api-key-here') {
			return this.getFallbackResponse(userMessage);
		}

		try {
			// Prepare conversation context
			const messages = [
				{
					role: 'system',
					content: `You are Zenturion, an AI productivity coach. You help users with:
					- Task management and productivity tips
					- Team collaboration and motivation
					- Goal setting and achievement tracking
					- Sprint planning and project management
					- Maintaining streaks and consistency
					- Work-life balance advice
					
					Keep responses helpful, encouraging, and actionable. Use emojis occasionally to be friendly.
					Responses should be 1-3 paragraphs maximum. Focus on practical advice.`
				},
				// Add conversation history (last 5 messages to keep context manageable)
				...conversationHistory.slice(-5).map(msg => ({
					role: msg.type === 'user' ? 'user' : 'assistant',
					content: msg.content
				})),
				{
					role: 'user',
					content: userMessage
				}
			];

			const response = await fetch(this.API_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${this.API_KEY}`
				},
				body: JSON.stringify({
					model: 'gpt-3.5-turbo',
					messages,
					max_tokens: 300,
					temperature: 0.7
				})
			});

			if (!response.ok) {
				throw new Error(`AI API error: ${response.status}`);
			}

			const data = await response.json();
			return data.choices[0]?.message?.content || this.getFallbackResponse(userMessage);

		} catch (error) {
			console.error('AI API Error:', error);
			return this.getFallbackResponse(userMessage);
		}
	},

	getFallbackResponse(userMessage: string): string {
		const message = userMessage.toLowerCase();
		
		// Context-aware fallback responses
		if (message.includes('sprint') || message.includes('plan')) {
			return "Great question about sprint planning! 🎯 I'd recommend starting with a clear goal definition, breaking tasks into manageable chunks, and setting realistic deadlines. Consider using the SMART criteria for your objectives. Would you like me to help you structure a specific sprint plan?";
		}
		
		if (message.includes('motivat') || message.includes('morale')) {
			return "Team motivation is crucial for success! 🚀 Try implementing regular check-ins, celebrating small wins, and creating shared goals. Recognition goes a long way - consider peer appreciation sessions or highlighting individual contributions. What specific challenges is your team facing?";
		}
		
		if (message.includes('productiv') || message.includes('efficien')) {
			return "Productivity optimization is all about finding your rhythm! 📊 I've noticed most people work best with time-blocking, the Pomodoro technique, or by tackling high-energy tasks during their peak hours. Try tracking your energy levels throughout the day to identify your optimal work periods.";
		}
		
		if (message.includes('streak') || message.includes('consistent')) {
			return "Maintaining consistency is key to long-term success! 🔥 The secret is starting small and building habits gradually. Even 5-10 minutes daily can create powerful momentum. What's one small habit you could commit to doing every day?";
		}
		
		if (message.includes('goal') || message.includes('target')) {
			return "Goal setting is an art! 🎯 I recommend the SMART framework: Specific, Measurable, Achievable, Relevant, and Time-bound. Break large goals into weekly milestones and celebrate progress along the way. What goal would you like to work on first?";
		}
		
		if (message.includes('task') || message.includes('quick')) {
			return "Quick tasks are perfect for maintaining momentum! ⚡ Try the 2-minute rule: if something takes less than 2 minutes, do it now. For your 30-minute window, consider organizing your workspace, updating documentation, or tackling small bug fixes. What area needs the most attention?";
		}

		// Default responses for general queries
		const defaultResponses = [
			"That's an excellent question! 🤖 Based on your productivity patterns, I'd suggest focusing on one key priority at a time. Consistency beats perfection every time. What's the most important thing you want to accomplish today?",
			
			"I love your proactive approach! 🌟 The key to sustainable productivity is balancing focused work with regular breaks. Try time-blocking your calendar and protecting your deep work sessions. What's your biggest productivity challenge right now?",
			
			"Great thinking! 🚀 Remember, small consistent actions lead to big results. I recommend starting with your most impactful task when your energy is highest. Would you like help prioritizing your current workload?",
			
			"That's the spirit of continuous improvement! 📈 Consider implementing a daily reflection practice - just 5 minutes to review what worked well and what could be better. Progress over perfection is the goal!",
			
			"Excellent question! 💡 The most successful people I've observed share one trait: they focus on systems rather than just goals. What system or routine could you implement to support your objectives?"
		];
		
		return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
	},

	// Generate contextual insights based on user data
	generateInsight(type: 'streak' | 'team' | 'productivity' | 'achievement'): string {
		const insights = {
			streak: [
				"You're building incredible momentum! 🔥 Your consistency is paying off - keep this energy going!",
				"Streak power activated! 💪 You're proving that small daily actions create big results.",
				"Your dedication is inspiring! 🌟 This streak shows your commitment to growth."
			],
			team: [
				"Strong teams communicate openly. 👥 Consider scheduling a team check-in to maintain connection.",
				"Collaboration thrives on clarity. 🤝 Make sure everyone knows their role and how they contribute.",
				"Team success starts with individual support. 💙 A quick 'how are you doing?' can make a big difference."
			],
			productivity: [
				"Your peak performance windows are valuable! ⚡ Protect your high-energy times for important work.",
				"Productivity isn't about being busy - it's about being effective. 🎯 Focus on impact over activity.",
				"Small optimizations compound! 📊 Even 1% improvements daily lead to dramatic results over time."
			],
			achievement: [
				"You're so close to your next milestone! 🏆 Every step forward counts toward your bigger vision.",
				"Achievement unlocked soon! 🎖️ Your persistence is about to pay off in a big way.",
				"Progress is happening! 🌱 Sometimes growth isn't visible until suddenly it is - keep going!"
			]
		};

		const typeInsights = insights[type];
		return typeInsights[Math.floor(Math.random() * typeInsights.length)];
	}
};
