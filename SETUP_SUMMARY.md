# Setup Summary

## ✅ What You Have Now

### Single Repository Structure
```
Ayame-Bot/
├── backend/          # Discord Bot (Deploy to Render)
├── frontend/         # Keep-Alive Dashboard (Deploy to Vercel)
├── DEPLOYMENT.md     # Step-by-step deployment guide
└── README.md         # Main documentation
```

## 🎯 Deployment Strategy

### Why Single Repo?
✅ Easy to manage
✅ Both services deploy from same code
✅ Frontend can ping backend automatically
✅ Simpler version control

### Architecture
```
GitHub Repo (Single)
    │
    ├─→ Render (Backend)
    │   └─ Discord Bot runs 24/7
    │
    └─→ Vercel (Frontend)
        └─ Pings backend every 14 mins
```

## 🚀 Quick Deploy Steps

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy Backend (Render)
- Go to Render Dashboard
- New → Blueprint
- Connect GitHub repo
- Render detects `backend/render.yaml`
- Add `BOT_TOKEN` environment variable
- Deploy!

**Result:** `https://ayame-bot.onrender.com`

### 3. Deploy Frontend (Vercel)
- Go to Vercel Dashboard
- New Project
- Import GitHub repo
- Root Directory: `frontend`
- Deploy!

**Result:** `https://ayame-bot.vercel.app`

### 4. Update Frontend URLs
Edit these files with your Render URL:
- `frontend/pages/api/ping.js`
- `frontend/pages/index.js`

Replace:
```javascript
'https://ayame-bot.onrender.com/health'
```

With your actual Render URL.

## 🔄 How Keep-Alive Works

1. **Frontend** (Vercel) runs 24/7 for free
2. **Frontend** pings **Backend** every 14 minutes
3. **Backend** (Render) stays awake (doesn't sleep)
4. **Discord Bot** runs continuously

**Why 14 minutes?**
Render free tier sleeps after 15 minutes of inactivity. Pinging every 14 minutes keeps it awake!

## 💰 Cost

**Total: $0/month**

- Render Free: 750 hours/month (enough for 24/7)
- Vercel Free: Unlimited for personal projects

## ✅ What's Already Configured

### Backend (`backend/render.yaml`)
- ✅ Root directory set to `backend`
- ✅ Health check endpoint: `/health`
- ✅ Port configured: `8080`
- ✅ Python runtime

### Frontend
- ✅ Auto-ping every 14 minutes
- ✅ Status dashboard
- ✅ Manual ping button
- ✅ Health monitoring

## 🎉 You're Ready!

Just follow [DEPLOYMENT.md](DEPLOYMENT.md) for detailed step-by-step instructions.

Your bot will run 24/7 completely free! 🚀
