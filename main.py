import os
import asyncio
import discord
import random
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
from aiohttp import web

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing!")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Year-round cozy vibes with simple kaomoji
base_statuses = [
    "eating mochi >w<",
    "watching anime ^_^",
    "sipping matcha :3",
    "slurping ramen >o<",
    "cuddling plushies <3",
    "chasing butterflies ~",
    "under the sakura <3",
    "wind chime dreams ~",
    "reading manga ^-^",
    "cozy kotatsu time ~",
    "being sleepy -_-",
    "headpats please owo",
    "nya~ =^.^=",
    "happy vibes :D",
    "daydreaming *.*"
]

def get_seasonal_statuses():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return ["building snow bunnies ^_^", "decorating bonsai <3"]
    elif month in [3, 4, 5]:
        return ["hanami picnic <3", "flying koinobori ~"]
    elif month in [6, 7, 8]:
        return ["watching fireworks *.*", "eating watermelon :3"]
    elif month in [9, 10, 11]:
        return ["leaf peeping ^-^", "carving pumpkins >o<"]
    return []

@bot.event
async def on_ready():
    logger.info(f"🤖 Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"📊 Bot is in {len(bot.guilds)} guild(s)")
    
    # Set initial DND status
    all_statuses = base_statuses + get_seasonal_statuses()
    status = random.choice(all_statuses)
    activity = discord.Activity(type=discord.ActivityType.watching, name=status)
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    logger.info(f"🔴 Status set to DND with activity: {status}")
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ Synced {len(synced)} command(s)")
        for cmd in synced:
            logger.info(f"   - /{cmd.name}")
    except Exception as e:
        logger.error(f"❌ Failed to sync commands: {e}")
        logger.error("   Make sure bot has 'applications.commands' scope!")
    
    rotate_status.start()

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: {error}")

@tasks.loop(seconds=60)
async def rotate_status():
    all_statuses = base_statuses + get_seasonal_statuses()
    status = random.choice(all_statuses)
    activity = discord.Activity(type=discord.ActivityType.watching, name=status)
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    logger.info(f"🔴 Status rotated to: {status}")

INITIAL_EXTENSIONS = [
    "cogs.post_commands",
    "cogs.autopost_commands",
    "cogs.admin_commands",
    "cogs.security_commands"
]

async def health_check(request):
    """Health check endpoint for Render."""
    return web.Response(text="Bot is running!")

async def start_web_server():
    """Start a simple web server for health checks."""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 8080)))
    await site.start()
    logger.info(f"🌐 Web server started on port {os.getenv('PORT', 8080)}")

async def main():
    async with bot:
        # Start web server for Render health checks
        await start_web_server()
        
        for ext in INITIAL_EXTENSIONS:
            try:
                await bot.load_extension(ext)
                logger.info(f"✅ Loaded: {ext}")
            except Exception as e:
                logger.error(f"❌ Failed to load {ext}: {e}")
        
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot shutting down gracefully...")
