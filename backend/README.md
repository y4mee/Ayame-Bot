# Ayame Bot - Backend

Discord bot with Activity XP tracking, NSFW content commands, and moderation tools.

## Features

- **Activity XP System**: Track user activity (Spotify, gaming, streaming) and reward with roles
- **NSFW Commands**: Image, GIF, and video posting with auto-post functionality
- **Moderation**: Ban, kick, timeout, purge, and role management
- **Security**: Anti-spam and anti-raid protection

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file in root directory:
```env
BOT_TOKEN=your_discord_bot_token_here
```

3. Run the bot:
```bash
python backend/main.py
```

## Commands

### Activity XP (Everyone)
- `/xp [user]` - Check XP and level
- `/rank [user]` - Detailed stats
- `/leaderboard [page]` - Top users
- `/top` - Quick top 10

### NSFW (Everyone, NSFW channels only)
- `/nsfwimg <category>` - Post image
- `/nsfwgif <category>` - Post GIF
- `/nsfwvdo <category>` - Post video
- `/autonsfwimg <category>` - Auto-post images
- `/autonsfwgif <category>` - Auto-post GIFs
- `/autonsfwvdo <category>` - Auto-post videos
- `/list` - Show categories

### XP Admin (Admins only)
- `/setxpsystem #channel create_roles:True/False theme:anime` - Setup XP
- `/setrewardrole <level> @role` - Add reward role & sync
- `/editrewardrole <level> @newrole` - Change reward role
- `/backupxp` - Export XP data

### Moderation (Admins only)
- `/ban <user> [reason]` - Ban member
- `/kick <user> [reason]` - Kick member
- `/timeout <user> <minutes>` - Timeout member
- `/purge <amount>` - Delete messages
- `/warn <user> <reason>` - Warn member
- `/role <user> @role <add/remove>` - Manage roles

### Security (Admins only)
- `/antispam <on/off>` - Toggle spam protection
- `/antiraid <on/off>` - Toggle raid protection
- `/securitylog #channel` - Set security logs

## Deployment

### Render
Use `render.yaml` for deployment configuration.

### Railway
Use `railway.json` for deployment configuration.

### Heroku
Use `Procfile` for deployment configuration.

## Project Structure

```
backend/
├── cogs/                    # Command modules
│   ├── activity_xp.py      # XP system
│   ├── autopost_commands.py # Auto-post NSFW
│   ├── post_commands.py    # Single NSFW posts
│   ├── admin_commands.py   # Moderation & help
│   └── security_commands.py # Security features
├── main.py                 # Bot entry point
├── database.py             # Database management
├── scraper.py              # Reddit scraper
├── eporner_fetcher.py      # Video fetcher
├── nsfw_data.py            # NSFW categories
└── requirements.txt        # Dependencies
```

## License

MIT
