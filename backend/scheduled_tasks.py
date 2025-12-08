"""
Scheduled tasks for GitHub Actions.
This script runs the periodic tasks that were previously handled by Vercel cron.
"""

import os
import asyncio
import discord
import random
import logging
from dotenv import load_dotenv
from datetime import datetime

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
    logger.error("❌ BOT_TOKEN is missing!")
    exit(1)

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

async def run_scheduled_tasks():
    """Run all scheduled tasks."""
    logger.info("🚀 Starting scheduled tasks...")
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    intents.presences = True
    
    bot = discord.Client(intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"✅ Connected as {bot.user}")
        
        # Rotate status
        all_statuses = base_statuses + get_seasonal_statuses()
        status = random.choice(all_statuses)
        activity = discord.Activity(type=discord.ActivityType.watching, name=status)
        await bot.change_presence(status=discord.Status.dnd, activity=activity)
        logger.info(f"🔄 Status rotated to: {status}")
        
        # Add your other scheduled tasks here
        # Example: database cleanup, data fetching, etc.
        
        await bot.close()
    
    try:
        await bot.start(BOT_TOKEN)
    except Exception as e:
        logger.error(f"❌ Error running scheduled tasks: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(run_scheduled_tasks())
        logger.info("✅ Scheduled tasks completed successfully")
    except Exception as e:
        logger.error(f"❌ Scheduled tasks failed: {e}")
        exit(1)
