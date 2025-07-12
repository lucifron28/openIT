// Environment configuration
export const env = {
	API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
};

// API helper functions
export const api = {
	async fetch(endpoint: string, options?: RequestInit) {
		const url = `${env.API_BASE_URL}${endpoint}`;
		const response = await fetch(url, {
			headers: {
				'Content-Type': 'application/json',
				...options?.headers
			},
			...options
		});
		return response;
	},

	async get(endpoint: string) {
		return this.fetch(endpoint);
	},

	async post(endpoint: string, data?: any) {
		return this.fetch(endpoint, {
			method: 'POST',
			body: data ? JSON.stringify(data) : undefined
		});
	},

	async put(endpoint: string, data?: any) {
		return this.fetch(endpoint, {
			method: 'PUT',
			body: data ? JSON.stringify(data) : undefined
		});
	},

	async delete(endpoint: string) {
		return this.fetch(endpoint, {
			method: 'DELETE'
		});
	}
};
