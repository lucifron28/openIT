<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api';
	
	/** @type {{
		id: number,
		name: string,
		webhook_type: string,
		webhook_url: string,
		project: number,
		project_name: string,
		event_types: string[],
		is_active: boolean,
		created_at: string
	}[]} */
	let webhookIntegrations: {
		id: number,
		name: string,
		webhook_type: string,
		webhook_url: string,
		project: number,
		project_name: string,
		event_types: string[],
		is_active: boolean,
		created_at: string
	}[] = [];
	/** @type {{
		id: number,
		webhook_integration_name: string,
		webhook_type: string,
		event_type: string,
		status: string,
		response_status_code?: number,
		error_message?: string,
		created_at: string,
		sent_at?: string
	}[]} */
	let notificationLogs: {
		id: number,
		webhook_integration_name: string,
		webhook_type: string,
		event_type: string,
		status: string,
		response_status_code?: number,
		error_message?: string,
		created_at: string,
		sent_at?: string
	}[] = [];
	let selectedTab = 'integrations';
	let showCreateForm = false;
	let loading = false;
	let editingWebhook: number | null = null;
	let editWebhookData: {
		name: string;
		webhook_url: string;
		event_types: string[];
		is_active: boolean;
	} = {
		name: '',
		webhook_url: '',
		event_types: [],
		is_active: true
	};
	
	let newWebhook: {
		name: string;
		webhook_type: string;
		webhook_url: string;
		project: number;
		event_types: string[];
		is_active: boolean;
	} = {
		name: '',
		webhook_type: 'discord',
		webhook_url: '',
		project: 1,
		event_types: [],
		is_active: true
	};
	
	let availableEventTypes = [
		{ value: 'task_completed', label: 'Task Completed', emoji: '✅', description: 'When a team member completes a task' },
		{ value: 'badge_earned', label: 'Badge Earned', emoji: '🏆', description: 'When a user earns a new achievement' },
		{ value: 'project_created', label: 'Project Created', emoji: '🚀', description: 'When a new project is created' },
		{ value: 'milestone_reached', label: 'Milestone Reached', emoji: '🎯', description: 'When project milestones are achieved' },
		{ value: 'daily_streak', label: 'Daily Streak', emoji: '🔥', description: 'When users maintain daily activity' }
	];
	
	let projects = [
		{ id: 1, name: 'Main Project' },
		{ id: 2, name: 'Side Project' }
	];
	
	onMount(async () => {
		await loadWebhookIntegrations();
		await loadNotificationLogs();
	});
	
	async function loadWebhookIntegrations() {
		try {
			const response = await api.get('/api/notifications/webhook-integrations/');
			
			if (response.ok) {
				const data = await response.json();
				webhookIntegrations = data.results.map((item: any) => ({
					id: item.id,
					name: item.name,
					webhook_type: item.webhook_type,
					webhook_url: item.webhook_url,
					project: item.project,
					project_name: item.project_name || 'Unknown Project',
					event_types: item.event_types,
					is_active: item.is_active,
					created_at: item.created_at
				}));
			} else {
				console.error('Failed to load webhook integrations:', response.status);
				webhookIntegrations = [
					{
						id: 1,
						name: 'Team Discord Notifications',
						webhook_type: 'discord',
						webhook_url: 'http://127.0.0.1:8000/api/gamification/test-webhook/',
						project: 1,
						project_name: 'Main Project',
						event_types: ['task_completed', 'badge_earned'],
						is_active: true,
						created_at: '2024-01-15T10:30:00Z'
					},
					{
						id: 2,
						name: 'Microsoft Teams Updates',
						webhook_type: 'teams',
						webhook_url: 'https://mseufeduph.webhook.office.com/webhookb2/1d1a0208-f69a-47ed-9c1b-8c29c5fc9769@ddedb3cc-596d-482b-8e8c-6cc149a7a7b7/IncomingWebhook/5ec48116891e40f892555aada9ae6afc/d8352f48-e96e-4321-800f-f998f9af400a/V2oRLGoTcP3E6na4tZPqC7jd9YyGPC1BtfFMotrI_nvQA1',
						project: 1,
						project_name: 'Main Project',
						event_types: ['task_completed', 'milestone_reached'],
						is_active: true,
						created_at: '2024-01-14T15:20:00Z'
					}
				];
			}
		} catch (error) {
			console.error('Error loading webhook integrations:', error);
			webhookIntegrations = [
				{
					id: 1,
					name: 'Team Discord Notifications',
					webhook_type: 'discord',
					webhook_url: 'https://discord.com/api/webhooks/CHANNEL_ID/TOKEN',
					project: 1,
					project_name: 'Main Project',
					event_types: ['task_completed', 'badge_earned'],
					is_active: true,
					created_at: '2024-01-15T10:30:00Z'
				},
				{
					id: 2,
					name: 'Microsoft Teams Updates',
					webhook_type: 'teams',
					webhook_url: 'https://mseufeduph.webhook.office.com/webhookb2/1d1a0208-f69a-47ed-9c1b-8c29c5fc9769@ddedb3cc-596d-482b-8e8c-6cc149a7a7b7/IncomingWebhook/5ec48116891e40f892555aada9ae6afc/d8352f48-e96e-4321-800f-f998f9af400a/V2oRLGoTcP3E6na4tZPqC7jd9YyGPC1BtfFMotrI_nvQA1',
					project: 1,
					project_name: 'Main Project',
					event_types: ['task_completed', 'milestone_reached'],
					is_active: true,
					created_at: '2024-01-14T15:20:00Z'
				}
			];
		}
	}
	
	async function loadNotificationLogs() {
		try {
			const response = await api.get('/api/notifications/notification-logs/');
			
			if (response.ok) {
				const data = await response.json();
				notificationLogs = data.map((item: any) => ({
					id: item.id,
					webhook_integration_name: item.webhook_integration?.name || 'Unknown Integration',
					webhook_type: item.webhook_integration?.webhook_type || 'unknown',
					event_type: item.event_type,
					status: item.status,
					response_status_code: item.response_status_code,
					error_message: item.error_message,
					created_at: item.created_at,
					sent_at: item.sent_at
				}));
			} else {
				console.error('Failed to load notification logs:', response.status);
				notificationLogs = [
					{
						id: 1,
						webhook_integration_name: 'Team Discord Notifications',
						webhook_type: 'discord',
						event_type: 'task_completed',
						status: 'sent',
						response_status_code: 204,
						created_at: '2024-01-15T14:30:00Z',
						sent_at: '2024-01-15T14:30:05Z'
					},
					{
						id: 2,
						webhook_integration_name: 'Microsoft Teams Updates',
						webhook_type: 'teams',
						event_type: 'badge_earned',
						status: 'failed',
						response_status_code: 400,
						error_message: 'Invalid webhook URL',
						created_at: '2024-01-15T13:15:00Z'
					},
					{
						id: 3,
						webhook_integration_name: 'Team Discord Notifications',
						webhook_type: 'discord',
						event_type: 'milestone_reached',
						status: 'sent',
						response_status_code: 204,
						created_at: '2024-01-15T12:00:00Z',
						sent_at: '2024-01-15T12:00:02Z'
					}
				];
			}
		} catch (error) {
			console.error('Error loading notification logs:', error);
			notificationLogs = [
				{
					id: 1,
					webhook_integration_name: 'Team Discord Notifications',
					webhook_type: 'discord',
					event_type: 'task_completed',
					status: 'sent',
					response_status_code: 204,
					created_at: '2024-01-15T14:30:00Z',
					sent_at: '2024-01-15T14:30:05Z'
				},
				{
					id: 2,
					webhook_integration_name: 'Microsoft Teams Updates',
					webhook_type: 'teams',
					event_type: 'badge_earned',
					status: 'failed',
					response_status_code: 400,
					error_message: 'Invalid webhook URL',
					created_at: '2024-01-15T13:15:00Z'
				},
				{
					id: 3,
					webhook_integration_name: 'Team Discord Notifications',
					webhook_type: 'discord',
					event_type: 'milestone_reached',
					status: 'sent',
					response_status_code: 204,
					created_at: '2024-01-15T12:00:00Z',
					sent_at: '2024-01-15T12:00:02Z'
				}
			];
		}
	}
	
	async function createWebhook() {
		if (!newWebhook.name || !newWebhook.webhook_url || newWebhook.event_types.length === 0) {
			alert('Please fill in all required fields');
			return;
		}
		
		const urlValidation = validateWebhookUrl(newWebhook.webhook_url, newWebhook.webhook_type);
		if (!urlValidation.isValid) {
			alert(urlValidation.error);
			return;
		}
		
		loading = true;
		
		try {
			const response = await api.post('/api/notifications/webhook-integrations/', {
				name: newWebhook.name.trim(),
				webhook_type: newWebhook.webhook_type,
				webhook_url: newWebhook.webhook_url.trim(),
				project: newWebhook.project,
				event_types: newWebhook.event_types,
				is_active: newWebhook.is_active
			});
			
			if (response.ok) {
				await loadWebhookIntegrations();
				
				newWebhook = {
					name: '',
					webhook_type: 'discord',
					webhook_url: '',
					project: 1,
					event_types: [],
					is_active: true
				};
				
				showCreateForm = false;
				alert('✅ Webhook integration created successfully!');
			} else {
				const errorData = await response.json();
				alert(`❌ Failed to create webhook: ${response.status}\n\nDetails: ${JSON.stringify(errorData)}`);
			}
		} catch (error) {
			console.error('Error creating webhook:', error);
			alert(`❌ Failed to create webhook integration: ${error instanceof Error ? error.message : 'Unknown error'}`);
		} finally {
			loading = false;
		}
	}
	
	async function testWebhook(webhookId: number) {
		loading = true;
		
		try {
			const webhook = webhookIntegrations.find(w => w.id === webhookId);
			if (!webhook) {
				throw new Error('Webhook not found');
			}
			
			const response = await api.post(`/api/notifications/webhook-integrations/${webhookId}/test/`, {
				test_message: `🧪 Test notification from AQuest!\n\nThis is a test message for ${webhook.name}.\n\nIf you see this message, your webhook integration is working correctly! 🎉`
			});
			
			if (response.ok) {
				const data = await response.json();
				
				await loadNotificationLogs();
				
				alert('✅ Test notification sent successfully! Check your Discord/Teams channel and the notification logs below.');
			} else {
				const errorData = await response.json();
				alert(`❌ Test failed: ${response.status} - ${response.statusText}\n\nDetails: ${errorData.error || 'Unknown error'}`);
			}
			
		} catch (error) {
			console.error('Webhook test error:', error);
			alert(`❌ Test failed: ${error instanceof Error ? error.message : 'Unknown error'}\n\nPlease check:\n1. Django server is running\n2. Webhook URL is correct\n3. You have internet connection`);
		} finally {
			loading = false;
		}
	}
	
	async function toggleWebhook(webhookId: number) {
		const webhook = webhookIntegrations.find(w => w.id === webhookId);
		if (webhook) {
			webhook.is_active = !webhook.is_active;
			webhookIntegrations = [...webhookIntegrations];
		}
	}
	
	function startEditWebhook(webhookId: number) {
		const webhook = webhookIntegrations.find(w => w.id === webhookId);
		if (webhook) {
			editingWebhook = webhookId;
			editWebhookData = {
				name: webhook.name,
				webhook_url: webhook.webhook_url,
				event_types: [...webhook.event_types],
				is_active: webhook.is_active
			};
		}
	}
	
	function cancelEditWebhook() {
		editingWebhook = null;
		editWebhookData = {
			name: '',
			webhook_url: '',
			event_types: [],
			is_active: true
		};
	}
	
	async function saveEditWebhook() {
		if (!editWebhookData.name.trim() || !editWebhookData.webhook_url.trim()) {
			alert('Please fill in all required fields');
			return;
		}
		
		const webhook = webhookIntegrations.find(w => w.id === editingWebhook);
		if (!webhook) {
			alert('Webhook not found');
			return;
		}
		
		const validation = validateWebhookUrl(editWebhookData.webhook_url, webhook.webhook_type);
		if (!validation.isValid) {
			alert(`Invalid webhook URL: ${validation.error}`);
			return;
		}
		
		loading = true;
		
		try {
			const response = await api.put(`/api/notifications/webhook-integrations/${editingWebhook}/`, {
				name: editWebhookData.name.trim(),
				webhook_type: webhook.webhook_type,
				webhook_url: editWebhookData.webhook_url.trim(),
				project: webhook.project || 1,
				event_types: editWebhookData.event_types,
				is_active: editWebhookData.is_active
			});
			
			if (response.ok) {
				await loadWebhookIntegrations();
				cancelEditWebhook();
				alert('✅ Webhook integration updated successfully!');
			} else {
				const errorData = await response.json();
				alert(`❌ Failed to update webhook: ${response.status}\n\nDetails: ${JSON.stringify(errorData)}`);
			}
		} catch (error) {
			console.error('Error updating webhook:', error);
			alert(`❌ Failed to update webhook integration: ${error instanceof Error ? error.message : 'Unknown error'}`);
		} finally {
			loading = false;
		}
	}
	
	function handleEditEventTypeChange(eventType: string) {
		if (editWebhookData.event_types.includes(eventType)) {
			editWebhookData.event_types = editWebhookData.event_types.filter(t => t !== eventType);
		} else {
			editWebhookData.event_types = [...editWebhookData.event_types, eventType];
		}
	}

	function getStatusColor(status: string) {
		switch (status) {
			case 'sent': return 'text-green-400';
			case 'failed': return 'text-red-400';
			case 'pending': return 'text-yellow-400';
			case 'retry': return 'text-orange-400';
			default: return 'text-slate-400';
		}
	}
	
	function getWebhookTypeIcon(type: string) {
		return type === 'discord' ? '🟦' : '🟨';
	}
	
	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleString();
	}
	
	function handleEventTypeChange(eventType: string) {
		if (newWebhook.event_types.includes(eventType)) {
			newWebhook.event_types = newWebhook.event_types.filter(t => t !== eventType);
		} else {
			newWebhook.event_types = [...newWebhook.event_types, eventType];
		}
	}
	
	function validateWebhookUrl(url: string, type: string): { isValid: boolean; error?: string } {
		url = url.trim();
		
		if (!url) {
			return { isValid: false, error: 'Webhook URL is required' };
		}
		
		try {
			new URL(url);
		} catch {
			return { isValid: false, error: 'Invalid URL format' };
		}
		
		if (type === 'discord') {
			if (!url.includes('discord.com/api/webhooks/')) {
				return { isValid: false, error: 'Invalid Discord webhook URL format' };
			}
			if (url.endsWith('/***') || url.includes('CHANNEL_ID') || url.includes('TOKEN')) {
				return { isValid: false, error: 'Please replace placeholder values with actual Discord webhook URL' };
			}
		} else if (type === 'teams') {
			if (!url.includes('webhook.office.com/') && !url.includes('outlook.office.com/webhook/')) {
				return { isValid: false, error: 'Invalid Microsoft Teams webhook URL format' };
			}
			if (url.endsWith('/***') || url.includes('WEBHOOK_ID') || url.includes('TOKEN')) {
				return { isValid: false, error: 'Please replace placeholder values with actual Teams webhook URL' };
			}
		}
		
		return { isValid: true };
	}
</script>

<svelte:head>
	<title>Webhook Settings - AQuest</title>
</svelte:head>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div>
			<h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
				Webhook Integrations 🔗
			</h1>
			<p class="text-slate-400 mt-1">Manage Discord and Microsoft Teams notifications</p>
		</div>
		
		<button 
			on:click={() => showCreateForm = true}
			class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all flex items-center gap-2"
		>
			<span class="text-sm">➕</span>
			Add Integration
		</button>
	</div>

	<!-- Tabs -->
	<div class="flex space-x-1 bg-slate-800 p-1 rounded-lg">
		<button 
			class="flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors {selectedTab === 'integrations' ? 'bg-purple-500 text-white' : 'text-slate-400 hover:text-white'}"
			on:click={() => selectedTab = 'integrations'}
		>
			🔗 Integrations
		</button>
		<button 
			class="flex-1 px-4 py-2 text-sm font-medium rounded-md transition-colors {selectedTab === 'logs' ? 'bg-purple-500 text-white' : 'text-slate-400 hover:text-white'}"
			on:click={() => selectedTab = 'logs'}
		>
			📊 Notification Logs
		</button>
	</div>

	<!-- Create Form Modal -->
	{#if showCreateForm}
		<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
			<div class="bg-slate-800 rounded-xl p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
				<div class="flex items-center justify-between mb-4">
					<h2 class="text-xl font-semibold text-white">Add Webhook Integration</h2>
					<button 
						on:click={() => showCreateForm = false}
						class="text-slate-400 hover:text-white text-xl"
					>
						✕
					</button>
				</div>
				
				<form on:submit|preventDefault={createWebhook} class="space-y-4">
					<div>
						<label for="webhook-name" class="block text-sm font-medium text-slate-300 mb-1">Name</label>
						<input 
							id="webhook-name"
							type="text" 
							bind:value={newWebhook.name}
							placeholder="e.g., Team Discord Notifications"
							class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
							required
						>
					</div>
					
					<div>
						<label for="webhook-type" class="block text-sm font-medium text-slate-300 mb-1">Type</label>
						<select 
							id="webhook-type"
							bind:value={newWebhook.webhook_type}
							class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
						>
							<option value="discord">🟦 Discord</option>
							<option value="teams">🟨 Microsoft Teams</option>
						</select>
					</div>
					
					<div>
						<label for="webhook-url" class="block text-sm font-medium text-slate-300 mb-1">Webhook URL</label>
						<input 
							id="webhook-url"
							type="url" 
							bind:value={newWebhook.webhook_url}
							placeholder={newWebhook.webhook_type === 'discord' ? 'https://discord.com/api/webhooks/...' : 'https://outlook.office.com/webhook/...'}
							class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
							required
						>
					</div>
					
					<div>
						<label for="webhook-project" class="block text-sm font-medium text-slate-300 mb-1">Project</label>
						<select 
							id="webhook-project"
							bind:value={newWebhook.project}
							class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
						>
							{#each projects as project}
								<option value={project.id}>{project.name || 'Unnamed Project'}</option>
							{/each}
						</select>
					</div>
					
					<fieldset>
						<legend class="block text-sm font-medium text-slate-300 mb-2">Event Types</legend>
						<div class="space-y-2">
							{#each availableEventTypes as eventType}
								<label class="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-700 cursor-pointer">
									<input 
										type="checkbox" 
										checked={newWebhook.event_types.includes(eventType.value)}
										on:change={() => handleEventTypeChange(eventType.value)}
										class="rounded border-slate-600 text-purple-500 focus:ring-purple-500"
									>
									<span class="text-lg">{eventType.emoji}</span>
									<div class="flex-1">
										<div class="text-white font-medium">{eventType.label}</div>
										<div class="text-xs text-slate-400">{eventType.description}</div>
									</div>
								</label>
							{/each}
						</div>
					</fieldset>
					
					<div class="flex items-center justify-between pt-4">
						<label class="flex items-center gap-2">
							<input 
								type="checkbox" 
								bind:checked={newWebhook.is_active}
								class="rounded border-slate-600 text-purple-500 focus:ring-purple-500"
							>
							<span class="text-sm text-slate-300">Active</span>
						</label>
						
						<div class="flex gap-2">
							<button 
								type="button"
								on:click={() => showCreateForm = false}
								class="px-4 py-2 text-slate-400 hover:text-white transition-colors"
							>
								Cancel
							</button>
							<button 
								type="submit" 
								disabled={loading}
								class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all disabled:opacity-50"
							>
								{loading ? 'Creating...' : 'Create'}
							</button>
						</div>
					</div>
				</form>
			</div>
		</div>
	{/if}

	<!-- Content -->
	{#if selectedTab === 'integrations'}
		<!-- Webhook Integrations -->
		<div class="space-y-4">
			{#each webhookIntegrations as webhook}
				<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl p-6 border border-slate-600">
					{#if editingWebhook === webhook.id}
						<!-- Edit Mode -->
						<div class="space-y-4">
							<div class="flex items-center justify-between">
								<h3 class="text-lg font-semibold text-white">Edit Webhook Integration</h3>
								<button 
									on:click={cancelEditWebhook}
									class="text-slate-400 hover:text-white text-xl"
								>
									✕
								</button>
							</div>
							
							<form on:submit|preventDefault={saveEditWebhook} class="space-y-4">
								<div>
									<label for="edit-webhook-name-{webhook.id}" class="block text-sm font-medium text-slate-300 mb-1">Name</label>
									<input 
										id="edit-webhook-name-{webhook.id}"
										type="text" 
										bind:value={editWebhookData.name}
										placeholder="e.g., Team Discord Notifications"
										class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
										required
									>
								</div>
								
								<div>
									<label for="edit-webhook-url-{webhook.id}" class="block text-sm font-medium text-slate-300 mb-1">Webhook URL</label>
									<input 
										id="edit-webhook-url-{webhook.id}"
										type="url" 
										bind:value={editWebhookData.webhook_url}
										placeholder={webhook.webhook_type === 'discord' ? 'https://discord.com/api/webhooks/...' : 'https://outlook.office.com/webhook/...'}
										class="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:border-purple-500 focus:outline-none"
										required
									>
								</div>
								
								<div>
									<fieldset>
										<legend class="block text-sm font-medium text-slate-300 mb-2">Event Types</legend>
										<div class="space-y-2">
											{#each availableEventTypes as eventType}
												<label class="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-700 cursor-pointer">
													<input 
														type="checkbox" 
														checked={editWebhookData.event_types.includes(eventType.value)}
														on:change={() => handleEditEventTypeChange(eventType.value)}
														class="rounded border-slate-600 text-purple-500 focus:ring-purple-500"
													>
													<span class="text-lg">{eventType.emoji}</span>
													<div class="flex-1">
														<div class="text-white font-medium">{eventType.label}</div>
														<div class="text-xs text-slate-400">{eventType.description}</div>
													</div>
												</label>
											{/each}
										</div>
									</fieldset>
								</div>
								
								<div class="flex items-center justify-between">
									<label class="flex items-center gap-2">
										<input 
											type="checkbox" 
											bind:checked={editWebhookData.is_active}
											class="rounded border-slate-600 text-purple-500 focus:ring-purple-500"
										>
										<span class="text-sm text-slate-300">Active</span>
									</label>
									
									<div class="flex gap-2">
										<button 
											type="button"
											on:click={cancelEditWebhook}
											class="px-4 py-2 text-slate-400 hover:text-white transition-colors"
										>
											Cancel
										</button>
										<button 
											type="submit" 
											disabled={loading}
											class="px-4 py-2 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all disabled:opacity-50"
										>
											{loading ? 'Saving...' : 'Save Changes'}
										</button>
									</div>
								</div>
							</form>
						</div>
					{:else}
						<!-- View Mode -->
						<div class="flex items-start justify-between">
							<div class="flex-1">
								<div class="flex items-center gap-3 mb-2">
									<span class="text-2xl">{getWebhookTypeIcon(webhook.webhook_type)}</span>
									<div>
										<h3 class="font-semibold text-white">{webhook.name || 'Unnamed Webhook'}</h3>
										<p class="text-sm text-slate-400 capitalize">{webhook.webhook_type || 'Unknown'} • {webhook.project_name || 'Unknown Project'}</p>
									</div>
									<div class="flex items-center gap-2">
										{#if webhook.is_active}
											<span class="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full border border-green-500/30">
												● Active
											</span>
										{:else}
											<span class="px-2 py-1 bg-slate-500/20 text-slate-400 text-xs rounded-full border border-slate-500/30">
												⏸ Inactive
											</span>
										{/if}
									</div>
								</div>
								
								<div class="mb-3">
									<p class="text-sm text-slate-400 mb-1">Webhook URL:</p>
									<code class="text-xs bg-slate-900 px-2 py-1 rounded text-slate-300 break-all">
										{webhook.webhook_url.replace(/\/[^/]+$/, '/***')}
									</code>
								</div>
								
								<div class="flex flex-wrap gap-2">
									{#each webhook.event_types as eventType}
										{@const eventInfo = availableEventTypes.find(e => e.value === eventType)}
										<span class="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-full border border-purple-500/30">
											{eventInfo?.emoji} {eventInfo?.label}
										</span>
									{/each}
								</div>
							</div>
							
							<div class="flex items-center gap-2 ml-4">
								<button 
									on:click={() => startEditWebhook(webhook.id)}
									class="px-3 py-1 bg-purple-500/20 text-purple-400 text-sm rounded-lg border border-purple-500/30 hover:bg-purple-500/30 transition-colors"
								>
									✏️ Edit
								</button>
								<button 
									on:click={() => testWebhook(webhook.id)}
									disabled={loading || !webhook.is_active}
									class="px-3 py-1 bg-blue-500/20 text-blue-400 text-sm rounded-lg border border-blue-500/30 hover:bg-blue-500/30 transition-colors disabled:opacity-50"
								>
									🧪 Test
								</button>
								<button 
									on:click={() => toggleWebhook(webhook.id)}
									class="px-3 py-1 bg-slate-500/20 text-slate-400 text-sm rounded-lg border border-slate-500/30 hover:bg-slate-500/30 transition-colors"
								>
									{webhook.is_active ? '⏸ Disable' : '▶ Enable'}
								</button>
							</div>
						</div>
						
						<div class="mt-4 pt-4 border-t border-slate-600 text-xs text-slate-400">
							Created: {formatDate(webhook.created_at)}
						</div>
					{/if}
				</div>
			{/each}
			
			{#if webhookIntegrations.length === 0}
				<div class="text-center py-12">
					<div class="text-6xl mb-4">🔗</div>
					<h3 class="text-xl font-semibold text-white mb-2">No Webhook Integrations</h3>
					<p class="text-slate-400 mb-4">Create your first webhook integration to start receiving notifications</p>
					<button 
						on:click={() => showCreateForm = true}
						class="px-6 py-3 bg-gradient-to-r from-purple-500 to-teal-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-teal-600 transition-all"
					>
						Add Integration
					</button>
				</div>
			{/if}
		</div>
		
	{:else if selectedTab === 'logs'}
		<!-- Notification Logs -->
		<div class="bg-gradient-to-br from-slate-800 to-slate-700 rounded-xl border border-slate-600 overflow-hidden">
			<div class="p-4 border-b border-slate-600">
				<h2 class="font-semibold text-white">Recent Notifications</h2>
				<p class="text-sm text-slate-400">Track the status of sent webhook notifications</p>
			</div>
			
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead class="bg-slate-900">
						<tr>
							<th class="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Integration</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Event</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Status</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Response</th>
							<th class="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase">Time</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-600">
						{#each notificationLogs as log}
							<tr class="hover:bg-slate-700/50">
								<td class="px-4 py-3">
									<div class="flex items-center gap-2">
										<span class="text-lg">{getWebhookTypeIcon(log.webhook_type)}</span>
										<div>
											<div class="text-sm font-medium text-white">{log.webhook_integration_name || 'Unknown Integration'}</div>
											<div class="text-xs text-slate-400 capitalize">{log.webhook_type || 'Unknown'}</div>
										</div>
									</div>
								</td>
								<td class="px-4 py-3">
									<span class="px-2 py-1 bg-slate-600 text-slate-300 text-xs rounded-full">
										{(log.event_type || 'unknown').replace('_', ' ')}
									</span>
								</td>
								<td class="px-4 py-3">
									<span class="px-2 py-1 text-xs rounded-full {(log.status === 'sent') ? 'bg-green-500/20 text-green-400' : (log.status === 'failed') ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'}">
										{log.status || 'pending'}
									</span>
								</td>
								<td class="px-4 py-3">
									<div class="text-sm text-slate-300">{log.response_status_code || 'N/A'}</div>
									{#if log.error_message}
										<div class="text-xs text-red-400 truncate max-w-xs" title={log.error_message}>
											{log.error_message}
										</div>
									{/if}
								</td>
								<td class="px-4 py-3">
									<div class="text-sm text-slate-300">{formatDate(log.created_at)}</div>
									{#if log.sent_at}
										<div class="text-xs text-slate-400">Sent: {formatDate(log.sent_at)}</div>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
			
			{#if notificationLogs.length === 0}
				<div class="text-center py-12">
					<div class="text-4xl mb-4">📊</div>
					<h3 class="text-lg font-semibold text-white mb-2">No Notification Logs</h3>
					<p class="text-slate-400">Notification history will appear here once webhooks start sending</p>
				</div>
			{/if}
		</div>
	{/if}

	<!-- Setup Instructions -->
	<div class="bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/20">
		<h3 class="font-semibold text-white mb-3 flex items-center gap-2">
			📋 Setup Instructions
		</h3>
		
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			<div>
				<h4 class="font-medium text-blue-300 mb-2">🟦 Discord Setup</h4>
				<ol class="text-sm text-slate-300 space-y-1 list-decimal list-inside mb-3">
					<li>Go to your Discord server settings</li>
					<li>Navigate to Integrations → Webhooks</li>
					<li>Create a new webhook and copy the URL</li>
					<li>Paste the URL in the form above</li>
				</ol>
				<div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
					<p class="text-xs text-blue-300 font-medium mb-1">💡 Pro Tip:</p>
					<p class="text-xs text-slate-300">Test button sends a real message to verify your webhook works correctly!</p>
				</div>
			</div>
			
			<div>
				<h4 class="font-medium text-yellow-300 mb-2">🟨 Microsoft Teams Setup</h4>
				<ol class="text-sm text-slate-300 space-y-1 list-decimal list-inside mb-3">
					<li>Go to your Teams channel</li>
					<li>Click ⋯ → Connectors</li>
					<li>Configure "Incoming Webhook"</li>
					<li>Copy the webhook URL and paste above</li>
				</ol>
				<div class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
					<p class="text-xs text-yellow-300 font-medium mb-1">⚠️ Common Issues:</p>
					<ul class="text-xs text-slate-300 space-y-1">
						<li>• Make sure URL doesn't have extra spaces</li>
						<li>• Don't include "/***" at the end</li>
						<li>• Webhook expires if not used for 90 days</li>
						<li>• Test button will send actual message to verify</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</div>
