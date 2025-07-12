import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import tailwindcs from "@tailwindcss/vite";

export default defineConfig({
	plugins: [sveltekit(), tailwindcs()]
});
