# Deployment Configuration

## ✅ ACTIVE DEPLOYMENT: Railway
- **URL**: https://bellavista-backend-production.up.railway.app
- **Status**: WORKING
- **Auto-deploy**: GitHub main branch
- **Config**: railway.json

## ❌ DISABLED: Render
- **Status**: REMOVED
- **Files deleted**: render.yaml, build.sh, start.sh
- **Ignore file**: .renderignore created
- **Action needed**: Disconnect Render webhook from GitHub repo

## 🔧 To Stop Render Deployment Emails:
1. Go to your GitHub repository settings
2. Navigate to Webhooks
3. Find and delete any Render webhooks
4. Or go to Render dashboard and disconnect the service

## 📍 Current Setup:
- **Primary**: Railway (working)
- **Secondary**: None (Render disabled)
- **Deployment**: Automatic on git push