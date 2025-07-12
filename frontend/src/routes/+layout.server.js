import { redirect } from '@sveltejs/kit';

// @ts-ignore
export const load = async ({ cookies, url }) => {
  const token = cookies.get('access_token'); // this must match your backend cookie!

  // Allow unauthenticated access on these pages
  if (url.pathname === '/login' || url.pathname === '/register') {
    return {};
  }
  // Redirect to login if not authenticated
  if (!token) {
    throw redirect(302, '/login');
  }
  return {};
};
