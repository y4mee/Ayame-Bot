# Troubleshooting Guide

## Common Issues and Solutions

---

## ❌ Error 429: Rate Limited by Discord

### Error Message:
```
discord.errors.HTTPException: 429 Too Many Requests
Error 1015: You are being rate limited
```

### What Happened:
Discord/Cloudflare temporarily blocked Render's IP due to too many login attempts.

### Solutions:

#### ✅ Solution 1: Wait (Recommended)
**Just wait 15-30 minutes.** Discord rate limits are temporary and will clear automatically.

#### ✅ Solution 2: Stop Redeploying
- Don't keep clicking "Manual Deploy" on Render
- Each deploy = new login attempt
- Too many attempts = rate limit

#### ✅ Solution 3: Check Your Bot Token
Make sure your `BOT_TOKEN` environment variable is correct:
1. Go to Render Dashboard
2. Your service → Environment
3. Check `BOT_TOKEN` value
4. If wrong, update it and redeploy

#### ✅ Solution 4: Use a Different Deployment Platform
If Render's IP is blocked for too long, try:
- Railway.app
- Fly.io
- Your own VPS

---

## ❌ Port Already in Use (Local)

### Error Message:
```
OSError: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8080)
```

### Solution:
Another bot instance is running. Close it:

**Windows:**
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Or just restart your computer** 😅

---

## ❌ Bot Not Responding to Commands

### Checklist:

1. **Check Bot is Online**
   - Visit: `https://your-render-url.onrender.com/health`
   - Should show: "Bot is running!"

2. **Check Discord Developer Portal**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Your bot → Bot → Privileged Gateway Intents
   - Enable: **Presence Intent**, **Server Members Intent**, **Message Content Intent**

3. **Check Bot Permissions**
   - Bot needs these permissions in your server:
     - Read Messages
     - Send Messages
     - Embed Links
     - Manage Roles
     - Kick/Ban Members (for moderation)

4. **Check Render Logs**
   - Go to Render Dashboard
   - Your service → Logs
   - Look for errors

---

## ❌ Commands Not Showing Up

### Solution:
Commands need to be synced with Discord.

**Wait 1-2 hours** for Discord to sync globally, or:

1. Kick bot from server
2. Re-invite with this URL:
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands
```

Replace `YOUR_BOT_ID` with your actual bot ID.

---

## ❌ XP Not Tracking

### Checklist:

1. **Presence Intent Enabled?**
   - Discord Developer Portal → Bot → Privileged Gateway Intents
   - Enable **Presence Intent**

2. **XP System Configured?**
   - Run: `/setxpsystem #channel create_roles:True`

3. **User Has Activity?**
   - XP only tracks real activities (Spotify, games, streaming)
   - Custom status does NOT count

4. **Check Logs**
   - Render Dashboard → Logs
   - Look for "Activity detected" messages

---

## ❌ Render Service Sleeping

### Symptoms:
- Bot goes offline after 15 minutes
- Commands don't work until you visit the URL

### Solution:
Deploy the frontend on Vercel to keep it awake!

See [DEPLOYMENT.md](DEPLOYMENT.md) Step 3.

The frontend will ping your backend every 14 minutes automatically.

---

## ❌ Frontend Not Pinging Backend

### Checklist:

1. **Update Render URL in Frontend**
   - Edit `frontend/pages/api/ping.js`
   - Edit `frontend/pages/index.js`
   - Replace `https://ayame-bot.onrender.com` with your actual URL

2. **Check Vercel Logs**
   - Vercel Dashboard → Your project → Functions
   - Check `/api/ping` logs

3. **Test Manually**
   - Visit: `https://your-vercel-url.vercel.app/api/ping`
   - Should show: `{"success": true, "botStatus": "online"}`

---

## ❌ Database Errors

### Error Message:
```
sqlite3.OperationalError: database is locked
```

### Solution:
This is normal on Render free tier. The bot will retry automatically.

If it persists:
1. Render Dashboard → Your service
2. Manual Deploy → Clear build cache & deploy

---

## ❌ NSFW Commands Not Working

### Checklist:

1. **Channel is NSFW?**
   - Discord → Channel Settings → Age-Restricted Channel (NSFW)
   - Toggle ON

2. **Bot Has Permissions?**
   - Bot needs: Send Messages, Embed Links

3. **Check Category**
   - Run: `/list` to see available categories
   - Use exact category name

---

## ❌ Buttons Not Working (Auto-post)

### Symptoms:
- Click ⟳ button, nothing happens
- Click 🗑️ button, nothing happens

### Solution:
Bot needs to restart to register button handlers.

**On Render:**
1. Dashboard → Your service
2. Manual Deploy

**Locally:**
Just restart the bot.

---

## 🆘 Still Having Issues?

### Check Logs:

**Render:**
```
Dashboard → Your service → Logs
```

**Vercel:**
```
Dashboard → Your project → Functions → Logs
```

**Local:**
Look at terminal output

### Common Log Messages:

✅ **Good:**
```
✅ Loaded: cogs.activity_xp
🤖 Logged in as YourBot
✅ Synced 32 command(s)
```

❌ **Bad:**
```
❌ Failed to load cogs.activity_xp
❌ BOT_TOKEN is missing!
❌ Rate limited by Discord
```

---

## 📞 Need More Help?

1. Check Render logs for errors
2. Check Vercel logs for ping issues
3. Verify all environment variables are set
4. Make sure Discord intents are enabled
5. Wait 15-30 minutes if rate limited

Most issues resolve themselves after waiting a bit! 😊
