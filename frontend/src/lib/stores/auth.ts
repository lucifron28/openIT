import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';

export interface User {
	id: number;
	username: string;
	email: string;
	first_name?: string;
	last_name?: string;
}

export interface AuthState {
	user: User | null;
	token: string | null;
	isAuthenticated: boolean;
	loading: boolean;
}

const initialState: AuthState = {
	user: null,
	token: null,
	isAuthenticated: false,
	loading: true
};

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>(initialState);

	return {
		subscribe,
		login: async (email: string, password: string) => {
			update(state => ({ ...state, loading: true }));
			
			try {
				const response = await fetch('http://localhost:8000/api/users/login/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ email, password }),
					credentials: 'include'
				});

				if (response.ok) {
					const data = await response.json();
					const authState = {
						user: data.user || { id: 1, username: email.split('@')[0], email },
						token: data.access,
						isAuthenticated: true,
						loading: false
					};
					
					// Store token in localStorage
					if (browser) {
						localStorage.setItem('auth_token', data.access);
					}
					
					set(authState);
					return { success: true };
				} else {
					const error = await response.json();
					update(state => ({ ...state, loading: false }));
					return { success: false, error: error.detail || 'Login failed' };
				}
			} catch (error) {
				update(state => ({ ...state, loading: false }));
				return { success: false, error: 'Network error' };
			}
		},
		
		register: async (email: string, username: string, password: string, confirm_password: string) => {
			update(state => ({ ...state, loading: true }));
			
			try {
				const response = await fetch('http://localhost:8000/api/users/register/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ email, username, password, confirm_password })
				});

				if (response.ok) {
					update(state => ({ ...state, loading: false }));
					return { success: true };
				} else {
					const error = await response.json();
					update(state => ({ ...state, loading: false }));
					return { success: false, error };
				}
			} catch (error) {
				update(state => ({ ...state, loading: false }));
				return { success: false, error: 'Network error' };
			}
		},
		
		logout: async () => {
			try {
				await fetch('http://localhost:8000/api/users/logout/', {
					method: 'POST',
					credentials: 'include',
					headers: {
						'Authorization': `Bearer ${get(auth).token}`
					}
				});
			} catch (error) {
				console.error('Logout error:', error);
			}
			
			// Clear local storage
			if (browser) {
				localStorage.removeItem('auth_token');
			}
			
			set({
				user: null,
				token: null,
				isAuthenticated: false,
				loading: false
			});
		},
		
		init: () => {
			if (!browser) return;
			
			const token = localStorage.getItem('auth_token');
			if (token) {
				// TODO: Validate token with backend
				update(state => ({
					...state,
					token,
					isAuthenticated: true,
					loading: false,
					user: { id: 1, username: 'user', email: 'user@example.com' }
				}));
			} else {
				update(state => ({ ...state, loading: false }));
			}
		}
	};
}

export const auth = createAuthStore();

// Get current auth state (for use in functions)
export function get(store: any) {
	let value: any;
	store.subscribe((val: any) => value = val)();
	return value;
}
