# Ayame Bot 🤖

A feature-rich Discord bot with NSFW content, moderation, and security features.

## ✨ Features

### 🔞 NSFW Commands (7 commands)
- `/post_image` - Post NSFW images
- `/post_gif` - Post NSFW gifs
- `/post_clip` - Post NSFW videos
- `/autopost_image` - Interactive image posting
- `/autopost_gif` - Interactive gif posting
- `/autopost_clip` - Interactive video posting
- `/list` - List all categories

### 🛡️ Admin Commands (14 commands)
- `/ban`, `/unban`, `/kick` - Member moderation
- `/timeout`, `/untimeout` - Timeout management
- `/purge`, `/clear` - Message management
- `/lock`, `/unlock` - Channel control
- `/slowmode` - Rate limiting
- `/nick`, `/role` - Member management
- `/warn` - Warning system
- `/serverinfo` - Server statistics

### 🔒 Security Commands (10 commands)
- `/security` - Enable/disable features
- `/setlog` - Configure logging
- `/setverify` - Setup verification
- `/verify_panel` - Send verification button
- `/antiraid` - Configure raid protection
- `/badwords` - Manage word filter
- `/lockdown`, `/unlock_server` - Emergency lockdown
- `/backup` - Server backup
- `/security_status` - View settings

### 🎨 Additional Features
- Seasonal status messages with kaomoji
- DND status (red circle)
- Auto-spam detection
- Anti-raid protection
- Anti-alt detection
- Bad words filter
- Verification system
- Audit logging

## 🚀 Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your bot token
4. Run: `python main.py`

## 📦 Requirements

- Python 3.11+
- Discord bot token
- NSFW channels for content commands

## 🌐 Deploy to Render

See [DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md) for detailed deployment guide.

## 📝 Configuration

All settings are per-server and saved automatically:
- Security features can be toggled with `/security`
- Logging channel set with `/setlog`
- Verification configured with `/setverify`

## 🔐 Security

- All admin commands require Administrator permission
- NSFW commands only work in NSFW channels
- Environment variables for sensitive data
- Automatic spam and raid detection

## 📊 Total Commands: 31

- 7 NSFW commands
- 14 Admin commands
- 10 Security commands

## 🆘 Support

For issues or questions, check the logs or documentation.

## 📄 License

This project is for educational purposes.
