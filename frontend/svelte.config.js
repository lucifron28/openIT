import adapter from '@sveltejs/adapter-vercel';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// Use Vercel adapter with explicit Node.js runtime
		adapter: adapter({
			runtime: 'nodejs20.x'
		})
	}
};

export default config;
