# Ayame Bot Keep-Alive Service

A Next.js app deployed on Vercel that automatically pings your Discord bot every 14 minutes to keep it awake on Render's free tier.

## 🚀 Features

- ✨ Automatic ping every 14 minutes using Vercel Cron Jobs
- 🎨 Beautiful status dashboard
- 🔄 Real-time bot status monitoring
- 📊 Manual ping button for testing
- 🌐 Deployed on Vercel (free tier)

## 📦 Deployment

### Deploy to Vercel (Recommended)

1. **Push to GitHub:**
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select the `frontend` folder as root directory
   - Click "Deploy"

3. **Enable Cron Jobs:**
   - Vercel will automatically detect `vercel.json`
   - Cron job will run every 14 minutes
   - Check logs in Vercel dashboard

### Alternative: Deploy Button

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/ayame-bot&project-name=ayame-bot-keepalive&root-directory=frontend)

## 🛠️ Local Development

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## ⚙️ Configuration

Edit `pages/api/ping.js` to change the bot URL:

```javascript
const BOT_URL = 'https://ayame-bot.onrender.com/health';
```

Edit `vercel.json` to change ping frequency:

```json
{
  "crons": [
    {
      "path": "/api/ping",
      "schedule": "*/14 * * * *"  // Every 14 minutes
    }
  ]
}
```

## 📊 How It Works

1. **Vercel Cron Job** runs every 14 minutes
2. Calls `/api/ping` endpoint
3. Endpoint fetches `https://ayame-bot.onrender.com/health`
4. Keeps bot awake on Render free tier
5. Dashboard shows real-time status

## 🎯 Why 14 Minutes?

- Render free tier sleeps after 15 minutes of inactivity
- Pinging every 14 minutes keeps it awake
- Vercel cron jobs are free and reliable

## 📝 Notes

- Vercel cron jobs require a Pro plan OR use external services like cron-job.org
- Alternative: Use GitHub Actions (free)
- Bot must have `/health` endpoint (already implemented)

## 🔗 Links

- Bot URL: https://ayame-bot.onrender.com
- Health Check: https://ayame-bot.onrender.com/health
- Dashboard: https://your-app.vercel.app

## 📄 License

MIT
