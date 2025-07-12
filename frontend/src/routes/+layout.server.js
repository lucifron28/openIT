import { redirect } from '@sveltejs/kit';

// @ts-ignore
export const load = async ({ cookies, url }) => {
  const token = cookies.get('access_token');

  if (url.pathname === '/login' || url.pathname === '/register') {
    return {};
  }
  if (!token) {
    throw redirect(302, '/login');
  }
  return {};
};
