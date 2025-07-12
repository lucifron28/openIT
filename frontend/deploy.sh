#!/bin/bash

# Vercel Deployment Script for Zentry Frontend

echo "🚀 Preparing Zentry Frontend for Vercel deployment..."

# Ensure we're in the frontend directory
cd "$(dirname "$0")"

# Test the build
echo "📦 Testing production build..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed! Please fix errors before deploying."
    exit 1
fi

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "initial: Zentry frontend for Vercel deployment"
else
    echo "📁 Adding changes to git..."
    git add .
    git commit -m "feat: configure frontend for Vercel deployment

- Updated SvelteKit config to use Vercel adapter
- Added environment variable configuration
- Created API helper with dynamic base URL
- Updated all API calls to use environment variables
- Added Vercel deployment configuration
- Ready for production deployment"
fi

echo "
🎉 Frontend is ready for Vercel deployment!

Next steps:
1. Push to GitHub: git push origin main
2. Connect repository to Vercel
3. Set environment variable: VITE_API_BASE_URL=https://your-backend-url
4. Deploy!

Or use Vercel CLI:
1. npm i -g vercel
2. vercel login
3. vercel --prod

📋 Don't forget to:
- Deploy your backend first (Railway/PythonAnywhere)
- Update VITE_API_BASE_URL with your backend URL
- Configure CORS in Django for your Vercel domain
"
