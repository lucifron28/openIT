import { redirect } from '@sveltejs/kit';

export async function handle({ event, resolve }) {
	// Proxy API requests to Django backend
	if (event.url.pathname.startsWith('/api/')) {
		const backendUrl = 'http://backend:8000' + event.url.pathname + event.url.search;
		
		const response = await fetch(backendUrl, {
			method: event.request.method,
			headers: {
				...Object.fromEntries(event.request.headers),
				// Ensure proper forwarding of auth headers
				'host': 'backend:8000',
			},
			body: event.request.method !== 'GET' && event.request.method !== 'HEAD' 
				? await event.request.text() 
				: undefined,
		});

		// Forward the response
		return new Response(response.body, {
			status: response.status,
			statusText: response.statusText,
			headers: response.headers,
		});
	}

	return resolve(event);
}
