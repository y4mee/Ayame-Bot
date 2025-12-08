# 🔧 Fix Python 3.13 Issue on Render

## Problem
Render is using Python 3.13 which doesn't have the `audioop` module that discord.py needs.

## Solution

### Option 1: Manual Configuration (RECOMMENDED)

1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add this environment variable:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.11.9`
5. Go to "Settings" tab
6. Under "Build Command", use:
   ```
   pip install --upgrade pip && pip install -r requirements.txt
   ```
7. Click "Manual Deploy" → "Deploy latest commit"

### Option 2: Use render.yaml

The render.yaml file has been updated with:
```yaml
envVars:
  - key: PYTHON_VERSION
    value: "3.11"
```

Push changes and redeploy.

### Option 3: Delete and Recreate Service

If the above doesn't work:

1. Delete the current Render service
2. Create a new one
3. When creating, manually set:
   - **Environment:** Python 3
   - **Python Version:** 3.11.9 (in Environment variables)
4. Add BOT_TOKEN environment variable
5. Deploy

## Verify Python Version

After deployment, check logs for:
```
Python 3.11.9
```

If you see Python 3.13, the version override didn't work.

## Alternative: Use Different Hosting

If Render keeps using Python 3.13:
- **Railway.app** - Better Python version control
- **Heroku** - Classic option
- **DigitalOcean** - VPS with full control

## Files Created

- `runtime.txt` - Specifies Python 3.11.9
- `.python-version` - Alternative version file
- `render.yaml` - Updated with Python version

## Quick Test Locally

```bash
python --version  # Should show 3.11.x
python main.py    # Should start without errors
```

## If Still Failing

Try this in Render dashboard:
1. Settings → Build Command:
   ```
   pip install discord.py==2.3.2 python-dotenv aiohttp
   ```
2. This installs only essential packages
3. Redeploy

The issue is specifically with Python 3.13 + discord.py compatibility.
