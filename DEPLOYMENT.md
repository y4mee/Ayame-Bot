# Deployment Guide

This guide shows how to deploy the bot backend on Render and frontend on Vercel from a single repository.

## 📋 Prerequisites

- GitHub account
- Render account (free)
- Vercel account (free)
- Discord Bot Token

---

## 🚀 Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## 🔧 Step 2: Deploy Backend on Render

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `backend/render.yaml`
5. Add environment variable:
   - `BOT_TOKEN` = your Discord bot token
6. Click **"Apply"**

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ayame-bot`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Add environment variables:
   - `BOT_TOKEN` = your Discord bot token
   - `PORT` = `8080`
6. Click **"Create Web Service"**

### Get Your Render URL

After deployment, you'll get a URL like:
```
https://ayame-bot.onrender.com
```

**Important:** Copy this URL! You'll need it for the frontend.

---

## 🌐 Step 3: Deploy Frontend on Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
   - **Build Command**: (leave default)
   - **Output Directory**: (leave default)
5. Click **"Deploy"**

### Update Frontend with Your Render URL

After both are deployed, update the frontend to use your actual Render URL:

1. Edit `frontend/pages/api/ping.js`:
```javascript
const BOT_URL = 'https://YOUR-RENDER-URL.onrender.com/health';
```

2. Edit `frontend/pages/index.js`:
```javascript
const response = await fetch('https://YOUR-RENDER-URL.onrender.com/health');
```

3. Push changes:
```bash
git add .
git commit -m "Update Render URL"
git push
```

Vercel will auto-deploy the changes.

---

## ✅ Step 4: Verify Everything Works

### Test Backend:
Visit: `https://YOUR-RENDER-URL.onrender.com/health`

Should show: `Bot is running!`

### Test Frontend:
Visit: `https://YOUR-VERCEL-URL.vercel.app`

Should show the keep-alive dashboard with bot status.

### Test Auto-Ping:
The frontend will automatically ping your backend every 14 minutes to keep it awake!

---

## 🔄 How It Works

```
┌─────────────────┐
│  Vercel         │
│  (Frontend)     │
│                 │
│  Auto-pings     │
│  every 14 mins  │
└────────┬────────┘
         │
         │ HTTP GET /health
         ▼
┌─────────────────┐
│  Render         │
│  (Backend)      │
│                 │
│  Discord Bot    │
│  Stays Awake ✅ │
└─────────────────┘
```

**Why 14 minutes?**
- Render free tier sleeps after 15 minutes of inactivity
- Pinging every 14 minutes keeps it awake
- Frontend runs 24/7 on Vercel (no sleep)

---

## 🛠️ Troubleshooting

### ⚠️ Error 429: Rate Limited
**Most common issue!**

If you see "429 Too Many Requests" or "Error 1015" in Render logs:
- **Solution:** Wait 15-30 minutes. Discord temporarily blocked Render's IP.
- **Cause:** Too many deploy attempts in short time
- **Prevention:** Don't keep clicking "Manual Deploy"

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Bot goes to sleep
- Check Vercel logs: Is the ping working?
- Check Render logs: Is the health endpoint responding?
- Verify the Render URL in frontend code is correct

### Bot not responding to commands
- Check Render logs for errors
- Verify `BOT_TOKEN` is set correctly
- Check Discord Developer Portal: Is Presence Intent enabled?

### Frontend not loading
- Check Vercel deployment logs
- Verify `frontend` directory structure is correct

**For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## 💰 Cost

**Total: $0/month**

- Render Free Tier: 750 hours/month (enough for 24/7 with keep-alive)
- Vercel Free Tier: Unlimited for personal projects
- Both services are completely free for this use case!

---

## 🔐 Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Set `BOT_TOKEN` as environment variable in Render
- Don't share your bot token publicly
- Keep your repository private if it contains sensitive data

---

## 📊 Monitoring

### Render Dashboard
- View logs: `https://dashboard.render.com/`
- Check uptime and performance
- Monitor memory usage

### Vercel Dashboard
- View deployment logs
- Check function invocations
- Monitor bandwidth

---

## 🎉 Done!

Your bot is now deployed and will stay awake 24/7!

- Backend: Running on Render
- Frontend: Running on Vercel
- Auto-ping: Keeping bot awake
- All from a single GitHub repository!

Need help? Check the logs in Render and Vercel dashboards.
