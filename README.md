# Ayame Bot - Discord Bot with Activity XP & Moderation

A feature-rich Discord bot with automatic activity tracking, XP system, moderation tools, and NSFW content commands.

## 📁 Project Structure

```
Ayame-Bot/
├── backend/          # Discord bot (Python)
│   ├── cogs/        # Command modules
│   ├── main.py      # Bot entry point
│   └── README.md    # Backend documentation
├── frontend/         # Keep-alive dashboard (Next.js)
│   └── README.md    # Frontend documentation
├── .env             # Environment variables
├── DEPLOYMENT.md    # Deployment guide
└── README.md        # This file
```

## 🚀 Features

### Activity XP System
- **Automatic tracking** of Spotify, games, streaming, and more
- **Random XP rewards** (3-20 XP per hour based on activity)
- **Streak bonuses** (2x multiplier per hour)
- **3 role themes** (Anime 🌸, Gaming 🎮, Ranks 🏆)
- **Leaderboards** and rank cards with reward roles

### Moderation Tools
- Ban, kick, timeout, warn members
- Purge messages, slowmode, lock channels
- Role and nickname management

### Security Features
- Anti-spam protection
- Anti-raid protection
- Security logging

### NSFW Commands
- Image, GIF, and video posting
- Auto-post with interactive ⟳ and 🗑️ buttons
- Multiple categories

## 📦 Quick Start (Local Development)

### Backend (Discord Bot)

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Setup environment:**
```bash
# Create .env in root directory
BOT_TOKEN=your_discord_bot_token_here
```

3. **Enable Presence Intent:**
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Select your bot → Bot → Privileged Gateway Intents
- Enable **Presence Intent** and **Server Members Intent**

4. **Run the bot:**
```bash
python backend/main.py
```

Or use the batch file:
```powershell
.\start.bat
```

### Frontend (Keep-Alive Dashboard)

See `frontend/README.md` for setup instructions.

## 🌐 Deployment (Production)

Deploy backend on **Render** and frontend on **Vercel** from a single repository.

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.**

### Quick Deploy:

1. **Push to GitHub**
2. **Deploy Backend on Render** (free tier)
   - Use `backend/render.yaml`
   - Add `BOT_TOKEN` environment variable
3. **Deploy Frontend on Vercel** (free tier)
   - Root directory: `frontend`
   - Auto-pings backend every 14 minutes to keep it awake

**Total Cost: $0/month** ✅

## 🎯 Quick Start Commands

### Setup Activity XP:
```
/setxpsystem #activity-log create_roles:True theme:anime
```

### Add custom reward role:
```
/setrewardrole 10 @Member
```

### Check your rank:
```
/rank
```

## 📋 Commands Summary

**Total Commands:** 32

### Everyone (12 commands)
- **Activity XP**: `/xp`, `/rank`, `/leaderboard`, `/top`
- **NSFW**: `/nsfwimg`, `/nsfwgif`, `/nsfwvdo`, `/autonsfwimg`, `/autonsfwgif`, `/autonsfwvdo`, `/list`
- **Info**: `/help`

### Admins Only (20 commands)
- **XP Admin**: `/setxpsystem`, `/setrewardrole`, `/editrewardrole`, `/backupxp`
- **Moderation**: `/ban`, `/unban`, `/kick`, `/timeout`, `/untimeout`, `/purge`, `/clear`, `/slowmode`, `/lock`, `/unlock`, `/nick`, `/role`, `/warn`
- **Security**: `/antispam`, `/antiraid`, `/securitylog`
- **Info**: `/serverinfo`

See `backend/README.md` for detailed command documentation.

## 🎨 Role Themes

Choose from 3 themes when setting up:

- **🌸 Anime**: Sakura Seed → Orb Ascendant
- **🎮 Gaming**: Noob → Mythic
- **🏆 Ranks**: Bronze I → Master

## 🔧 Configuration

### Required Permissions:
- Read Messages
- Send Messages
- Embed Links
- Manage Roles
- Kick Members
- Ban Members
- Moderate Members
- Manage Messages
- Manage Channels

### Required Intents:
- Presence Intent (for activity tracking)
- Server Members Intent (for anti-raid)
- Message Content Intent

## 📊 Database

Uses SQLite for data storage:
- `backend/bot_database.db` - Main database file
- Stores XP, levels, streaks, roles, and configuration
- Automatic backup with `/backupxp`

## 📝 Environment Variables

```env
BOT_TOKEN=your_discord_bot_token_here
PORT=8080  # Optional, for web server health checks
```

## 🤝 Support

For issues or questions:
1. Check bot has required permissions
2. Verify Presence Intent is enabled
3. Check logs for errors
4. See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help

## 📄 License

MIT License - Feel free to use and modify!

## 🎉 Credits

Built with discord.py and love ❤️
