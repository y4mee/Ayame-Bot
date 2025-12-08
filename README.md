# Ayame Bot - Discord Activity XP & Moderation Bot

A Discord bot that tracks user activity (Spotify, gaming, streaming) and rewards them with XP and roles. Includes moderation tools, security features, and NSFW content commands.

---

## 🚀 Quick Start

### Local Setup

1. **Install Python 3.11+**

2. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Create `.env` file in root:**
```env
BOT_TOKEN=your_discord_bot_token_here
```

4. **Enable Discord Intents:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Your Bot → Bot → Privileged Gateway Intents
   - Enable: **Presence Intent**, **Server Members Intent**, **Message Content Intent**

5. **Run:**
```bash
python backend/main.py
```

---

## 📋 Commands

### **Activity XP (Everyone)**
Use in designated XP channel

| Command | Usage | Description |
|---------|-------|-------------|
| `/xp` | `/xp [user]` | Check XP and level |
| `/rank` | `/rank [user]` | Detailed stats with progress |
| `/leaderboard` | `/leaderboard [page]` | Top users |
| `/top` | `/top` | Quick top 10 |
| `/rewardslist` | `/rewardslist` | View all reward roles |

### **NSFW (Everyone, NSFW channels only)**

| Command | Usage | Description |
|---------|-------|-------------|
| `/nsfwimg` | `/nsfwimg <category>` | Single image |
| `/nsfwgif` | `/nsfwgif <category>` | Single GIF |
| `/nsfwvdo` | `/nsfwvdo <category>` | Single video |
| `/autonsfwimg` | `/autonsfwimg <category>` | Auto-post images with ⟳ button |
| `/autonsfwgif` | `/autonsfwgif <category>` | Auto-post GIFs with ⟳ button |
| `/autonsfwvdo` | `/autonsfwvdo <category>` | Auto-post videos with ⟳ button |
| `/list` | `/list` | Show all categories |

**Categories:** hentai, neko, waifu, blowjob, pussy, anal, boobs, feet, thigh, etc.

### **XP Admin (Admins Only)**

| Command | Usage | Description |
|---------|-------|-------------|
| `/setxpsystem` | `/setxpsystem #channel create_roles:True/False` | Setup XP system |
| `/setrewardrole` | `/setrewardrole <level> @role` | Set/update reward role |
| `/backupxp` | `/backupxp` | Export XP database |
| `/resetxpsystem` | `/resetxpsystem` | Reset all XP data (with confirmation) |

**Note:** If `create_roles=True`, you'll be asked to choose a theme (Anime/Gaming/Ranks). If `False`, no theme selection.

### **Moderation (Admins Only)**

| Command | Usage | Description |
|---------|-------|-------------|
| `/ban` | `/ban <user> [reason]` | Ban member |
| `/kick` | `/kick <user> [reason]` | Kick member |
| `/timeout` | `/timeout <user> <minutes>` | Timeout member |
| `/purge` | `/purge <amount>` | Delete messages (1-100) |
| `/warn` | `/warn <user> <reason>` | Warn member via DM |
| `/role` | `/role <user> @role <add/remove>` | Manage roles |
| `/lock` | `/lock` | Lock channel |
| `/unlock` | `/unlock` | Unlock channel |

### **Security (Admins Only)**

| Command | Usage | Description |
|---------|-------|-------------|
| `/antispam` | `/antispam <on/off>` | Toggle spam protection |
| `/antiraid` | `/antiraid <on/off>` | Toggle raid protection |
| `/securitylog` | `/securitylog #channel` | Set security logs |

### **Info (Everyone)**

| Command | Usage | Description |
|---------|-------|-------------|
| `/help` | `/help` | Show all commands |

---

## 🎯 Setup Guide

### **Step 1: Setup XP System**

**Option A: With Auto-Roles (Recommended)**
```
/setxpsystem #xp-log create_roles:True theme:anime
```
- Bot creates themed roles automatically (Level 5, 10, 15, etc.)
- Choose theme: Anime 🌸, Gaming 🎮, or Ranks 🏆

**Option B: Manual Roles**
```
/setxpsystem #xp-log create_roles:False
```
- No auto-roles created
- You add roles manually using `/setrewardrole`

### **Step 2: Add Custom Reward Roles (If Manual)**
```
/setrewardrole 5 @Bronze
/setrewardrole 10 @Silver
/setrewardrole 20 @Gold
```
- Automatically syncs to all qualifying users
- Removes old roles when updating

### **Step 3: Users Check Their Progress**
```
/xp
/rank
/leaderboard
```

---

## 🎨 How XP Works

### **Activities Tracked:**
- 🎵 **Spotify** - 3-8 XP/hour
- 🎮 **Gaming** - 8-15 XP/hour
- 📺 **Streaming** - 12-20 XP/hour
- 🏆 **Competing** - 10-18 XP/hour

### **What's NOT Tracked:**
- ❌ Custom status (doesn't count)
- ❌ Bots (excluded automatically)
- ❌ Users from other servers

### **Streak Bonus:**
- 1st hour: 1x XP
- 2nd hour: 2x XP
- 3rd hour: 3x XP
- And so on...

### **Leveling:**
- 100 XP per level
- Level 1 = 100 XP
- Level 2 = 200 XP
- Level 10 = 1,000 XP

---

## 🌐 Deployment (Free 24/7 Hosting)

### **Backend: Render**

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. New → Blueprint
4. Connect GitHub repo
5. Render detects `backend/render.yaml`
6. Add environment variable: `BOT_TOKEN=your_token`
7. Deploy

**Your bot URL:** `https://your-app.onrender.com`

### **Frontend: Vercel (Keep-Alive)**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. New Project → Import GitHub repo
3. Root Directory: `frontend`
4. Deploy

**Update frontend files with your Render URL:**
- `frontend/pages/api/ping.js`
- `frontend/pages/index.js`

Replace `https://ayame-bot.onrender.com` with your actual URL.

**Result:** Frontend pings backend every 14 minutes to keep it awake!

---

## 🛠️ Troubleshooting

### **Error 429: Rate Limited**
**Cause:** Too many deploy attempts on Render
**Solution:** Wait 30-60 minutes. Discord will unblock the IP automatically.
**Prevention:** Don't spam "Manual Deploy" button

### **Bot Not Responding**
1. Check bot is online: Visit `https://your-render-url.onrender.com/health`
2. Verify `BOT_TOKEN` in Render environment variables
3. Check Discord Developer Portal: Presence Intent enabled?
4. Check bot has proper permissions in server

### **Commands Not Showing**
1. Wait 1-2 hours for Discord to sync
2. Or kick bot and re-invite with this URL:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands
```

### **XP Not Tracking**
1. Presence Intent enabled in Discord Developer Portal?
2. XP system configured? Run `/setxpsystem`
3. User has real activity? (Custom status doesn't count)
4. Check Render logs for errors

### **Render Service Sleeping**
Deploy frontend on Vercel - it will ping backend every 14 minutes to keep it awake.

### **Port Already in Use (Local)**
Another bot instance is running. Close it:
```powershell
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

---

## 📊 Project Structure

```
Ayame-Bot/
├── backend/              # Discord bot (Python)
│   ├── cogs/            # Command modules
│   │   ├── activity_xp.py
│   │   ├── autopost_commands.py
│   │   ├── post_commands.py
│   │   ├── admin_commands.py
│   │   └── security_commands.py
│   ├── main.py          # Bot entry point
│   ├── database.py      # SQLite database
│   ├── requirements.txt # Dependencies
│   └── render.yaml      # Render config
├── frontend/            # Keep-alive dashboard (Next.js)
│   ├── pages/
│   └── package.json
├── .env                 # Environment variables
└── README.md           # This file
```

---

## 🔐 Required Permissions

**Bot Permissions:**
- Read Messages
- Send Messages
- Embed Links
- Manage Roles
- Kick Members
- Ban Members
- Moderate Members
- Manage Messages
- Manage Channels

**Discord Intents:**
- Presence Intent (for activity tracking)
- Server Members Intent (for anti-raid)
- Message Content Intent

---

## 💰 Cost

**Total: $0/month**

- Render Free: 750 hours/month (enough for 24/7 with keep-alive)
- Vercel Free: Unlimited for personal projects

---

## 📝 Environment Variables

```env
BOT_TOKEN=your_discord_bot_token_here
PORT=8080  # Optional, for health checks
```

---

## 🎉 Features

- ✅ Automatic activity tracking (Spotify, gaming, streaming)
- ✅ XP and leveling system with reward roles
- ✅ 3 themed role sets (Anime, Gaming, Ranks)
- ✅ Leaderboards and rank cards
- ✅ Moderation tools (ban, kick, timeout, purge)
- ✅ Security features (anti-spam, anti-raid)
- ✅ NSFW content commands with auto-post
- ✅ Free 24/7 hosting on Render + Vercel
- ✅ Excludes bots automatically
- ✅ Per-server configuration

---

## 📄 License

MIT License - Free to use and modify!

---

## 🆘 Need Help?

1. Check Render logs: Dashboard → Your service → Logs
2. Check Vercel logs: Dashboard → Your project → Functions
3. Verify environment variables are set
4. Make sure Discord intents are enabled
5. If rate limited, wait 30-60 minutes

**Most issues resolve by waiting or checking logs!**
