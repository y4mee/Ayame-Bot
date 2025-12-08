# 🚀 Deployment Guide - Keep Bot Alive

## Option 1: GitHub Actions (100% Free, Recommended)

### Setup:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add keep-alive system"
   git push
   ```

2. **Enable GitHub Actions:**
   - Go to your GitHub repository
   - Click "Actions" tab
   - Enable workflows if prompted
   - The workflow will run automatically every 14 minutes

3. **Manual Test:**
   - Go to Actions tab
   - Click "Keep Bot Alive"
   - Click "Run workflow"
   - Check logs to verify it works

### Pros:
- ✅ Completely free
- ✅ No credit card required
- ✅ Reliable
- ✅ Easy to monitor (GitHub Actions logs)

### Cons:
- ⚠️ Minimum interval is 5 minutes (we use 14)
- ⚠️ May have slight delays

---

## Option 2: Vercel Deployment (Free with Limitations)

### Setup:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   npm install
   vercel
   ```

3. **Follow prompts:**
   - Login to Vercel
   - Select project settings
   - Deploy!

### Important Notes:
- ⚠️ Vercel Cron Jobs require **Pro plan** ($20/month)
- ✅ Free tier: Deploy the dashboard only
- ✅ Use GitHub Actions for actual pinging

### Alternative: Use the Dashboard Only
- Deploy frontend to Vercel for monitoring
- Use GitHub Actions for pinging
- Best of both worlds!

---

## Option 3: External Cron Service (Free)

### Using cron-job.org:

1. **Go to [cron-job.org](https://cron-job.org)**
2. **Create free account**
3. **Create new cron job:**
   - Title: "Keep Ayame Bot Alive"
   - URL: `https://ayame-bot.onrender.com/health`
   - Schedule: Every 14 minutes
   - Save

### Pros:
- ✅ Free
- ✅ Simple
- ✅ Reliable

### Cons:
- ⚠️ No custom dashboard
- ⚠️ External service dependency

---

## Option 4: UptimeRobot (Free)

### Setup:

1. **Go to [uptimerobot.com](https://uptimerobot.com)**
2. **Create free account**
3. **Add new monitor:**
   - Monitor Type: HTTP(s)
   - Friendly Name: Ayame Bot
   - URL: `https://ayame-bot.onrender.com/health`
   - Monitoring Interval: 5 minutes (free tier)

### Pros:
- ✅ Free
- ✅ Email alerts
- ✅ Status page
- ✅ Uptime statistics

### Cons:
- ⚠️ Minimum 5 minutes interval (free tier)

---

## Recommended Setup

### Best Configuration:

1. **Use GitHub Actions** for pinging (free, reliable)
2. **Deploy frontend to Vercel** for monitoring dashboard (free)
3. **Optional: Add UptimeRobot** for alerts

### Steps:

```bash
# 1. Enable GitHub Actions (already done)
git push

# 2. Deploy frontend to Vercel
cd frontend
npm install
vercel

# 3. Done! Bot stays awake 24/7
```

---

## Testing

### Test GitHub Actions:
```bash
# Check if workflow is running
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
```

### Test Bot Health:
```bash
curl https://ayame-bot.onrender.com/health
# Should return: "Bot is running!"
```

### Test Frontend:
```bash
cd frontend
npm install
npm run dev
# Open: http://localhost:3000
```

---

## Monitoring

### GitHub Actions Logs:
- Go to repository → Actions tab
- Click on latest workflow run
- View logs to see ping results

### Vercel Dashboard:
- Go to your deployed URL
- See real-time bot status
- Manual ping button for testing

---

## Troubleshooting

### Bot Still Sleeping?
- Check GitHub Actions is enabled
- Verify workflow runs every 14 minutes
- Check bot health endpoint works

### GitHub Actions Not Running?
- Enable Actions in repository settings
- Check workflow file syntax
- Verify cron schedule format

### Vercel Deployment Failed?
- Check Node.js version compatibility
- Verify package.json is correct
- Check Vercel logs for errors

---

## Cost Breakdown

| Service | Cost | Features |
|---------|------|----------|
| GitHub Actions | **FREE** | Unlimited public repos |
| Vercel (Free Tier) | **FREE** | Dashboard only |
| Vercel (Pro) | $20/month | Cron jobs included |
| cron-job.org | **FREE** | Basic cron jobs |
| UptimeRobot | **FREE** | 50 monitors, 5min interval |

**Recommended: GitHub Actions (100% Free!)**

---

## Final Structure

```
Ayame-Bot/
├── .github/
│   └── workflows/
│       └── keep-alive.yml    ← Pings every 14 min (FREE)
├── frontend/
│   ├── pages/
│   │   ├── index.js          ← Dashboard
│   │   └── api/
│   │       └── ping.js       ← API endpoint
│   ├── package.json
│   └── vercel.json           ← Vercel config
├── cogs/
├── main.py
└── README.md
```

---

## Support

Need help? Check:
- GitHub Actions logs
- Vercel deployment logs
- Bot logs on Render
- Health endpoint: https://ayame-bot.onrender.com/health

---

**Your bot will now stay awake 24/7! 🎉**
