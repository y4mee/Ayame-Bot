import os
import asyncio
import discord
import random
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
from aiohttp import web
from recovery import restore_guild_configs, verify_bot_health

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
intents.presences = True  # Required to see user activities (Spotify, games, etc.)

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
    
    # Restore guild configurations on startup
    logger.info("🔄 Restoring guild configurations...")
    await restore_guild_configs(bot)
    
    # Verify bot health
    await verify_bot_health(bot)
    
    # Set initial DND status
    all_statuses = base_statuses + get_seasonal_statuses()
    status = random.choice(all_statuses)
    activity = discord.Activity(type=discord.ActivityType.watching, name=status)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    logger.info(f" Status set to idle with activity: {status}")
    
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
    health_check_task.start()

@bot.event
async def on_guild_join(guild):
    """Handle bot joining a new server - request permissions and send setup guide."""
    logger.info(f"🎉 Bot joined new server: {guild.name} (ID: {guild.id})")
    
    # Required permissions for full functionality
    required_permissions = discord.Permissions(
        read_messages=True,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        manage_messages=True,  # For purge command
        manage_roles=True,     # For XP role assignment
        kick_members=True,     # For moderation
        ban_members=True,      # For moderation
        moderate_members=True, # For timeout/mute
        manage_channels=True,  # For lock/unlock
        view_channel=True
    )
    
    # Check current permissions
    bot_member = guild.get_member(bot.user.id)
    current_perms = bot_member.guild_permissions
    
    missing_perms = []
    if not current_perms.read_messages:
        missing_perms.append("Read Messages")
    if not current_perms.send_messages:
        missing_perms.append("Send Messages")
    if not current_perms.embed_links:
        missing_perms.append("Embed Links")
    if not current_perms.manage_roles:
        missing_perms.append("Manage Roles")
    if not current_perms.kick_members:
        missing_perms.append("Kick Members")
    if not current_perms.ban_members:
        missing_perms.append("Ban Members")
    if not current_perms.moderate_members:
        missing_perms.append("Moderate Members")
    
    # Try to find a channel to send welcome message
    welcome_channel = None
    
    # Try system channel first
    if guild.system_channel and guild.system_channel.permissions_for(bot_member).send_messages:
        welcome_channel = guild.system_channel
    else:
        # Find first text channel bot can send to
        for channel in guild.text_channels:
            if channel.permissions_for(bot_member).send_messages:
                welcome_channel = channel
                break
    
    if welcome_channel:
        embed = discord.Embed(
            title="👋 Thanks for adding me!",
            description="I'm ready to help manage your server with Activity XP tracking, moderation, and more!",
            color=discord.Color.purple()
        )
        
        # Permission status
        if missing_perms:
            embed.add_field(
                name="⚠️ Missing Permissions",
                value=f"I'm missing some permissions:\n• " + "\n• ".join(missing_perms) +
                      f"\n\n**Please grant these permissions for full functionality!**\n"
                      f"[Click here to re-invite with permissions]({discord.utils.oauth_url(bot.user.id, permissions=required_permissions)})",
                inline=False
            )
        else:
            embed.add_field(
                name="✅ All Permissions Granted",
                value="I have all the permissions I need!",
                inline=False
            )
        
        # Quick start guide
        embed.add_field(
            name="🚀 Quick Start",
            value="1. Run `/setxpsystem @role #channel rewardroles:Auto theme:gaming`\n"
                  "2. Use `/help` to see all commands\n"
                  "3. Users can check their rank with `/rank`",
            inline=False
        )
        
        # Important notes
        embed.add_field(
            name="⚠️ Important",
            value="• **Enable Presence Intent** in Discord Developer Portal\n"
                  "• Required for activity tracking (Spotify, games, etc.)\n"
                  "• Bot Settings → Privileged Gateway Intents → Presence Intent",
            inline=False
        )
        
        embed.set_footer(text="Use /help to see all available commands")
        
        try:
            await welcome_channel.send(embed=embed)
            logger.info(f"✅ Sent welcome message to {guild.name}")
        except Exception as e:
            logger.error(f"❌ Failed to send welcome message: {e}")
    else:
        logger.warning(f"⚠️ No channel found to send welcome message in {guild.name}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: {error}")
    try:
        await ctx.send(f"❌ An error occurred: {str(error)[:100]}")
    except:
        pass

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle slash command errors gracefully."""
    logger.error(f"Slash command error in {interaction.command.name}: {error}")
    try:
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"❌ An error occurred: {str(error)[:100]}",
                ephemeral=True
            )
    except Exception as e:
        logger.error(f"Failed to send error message: {e}")

@tasks.loop(seconds=60)
async def rotate_status():
    all_statuses = base_statuses + get_seasonal_statuses()
    status = random.choice(all_statuses)
    activity = discord.Activity(type=discord.ActivityType.watching, name=status)
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    logger.info(f"🔴 Status rotated to: {status}")

@tasks.loop(minutes=30)
async def health_check_task():
    """Periodic health check to ensure bot is functioning."""
    try:
        await verify_bot_health(bot)
    except Exception as e:
        logger.error(f"Health check failed: {e}")

INITIAL_EXTENSIONS = [
    "cogs.post_commands",
    "cogs.autopost_commands",
    "cogs.admin_commands",
    "cogs.security_commands",
    "cogs.activity_xp"
]

async def health_check(request):
    """Health check endpoint for Render."""
    return web.Response(text="Bot is running!")

async def start_web_server():
    """Start a simple web server for health checks (optional for deployment)."""
    try:
        app = web.Application()
        app.router.add_get('/', health_check)
        app.router.add_get('/health', health_check)
        
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.getenv('PORT', 8080))
        site = web.TCPSite(runner, '0.0.0.0', port)
        await site.start()
        logger.info(f"🌐 Web server started on port {port}")
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            logger.warning(f"⚠️ Port {port} already in use, skipping web server (bot will still work)")
        else:
            logger.error(f"❌ Failed to start web server: {e}")
    except Exception as e:
        logger.error(f"❌ Web server error: {e}")

async def main():
    async with bot:
        # Start web server for deployment health checks (optional)
        await start_web_server()
        
        for ext in INITIAL_EXTENSIONS:
            try:
                await bot.load_extension(ext)
                logger.info(f"✅ Loaded: {ext}")
            except Exception as e:
                logger.error(f"❌ Failed to load {ext}: {e}")
        
        # Start bot with retry logic for rate limits
        max_retries = 3
        retry_delay = 60  # seconds
        
        for attempt in range(max_retries):
            try:
                await bot.start(BOT_TOKEN)
                break  # Success, exit retry loop
            except discord.errors.HTTPException as e:
                if e.status == 429:  # Rate limited
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ Rate limited by Discord. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        logger.error("❌ Rate limit exceeded. Please wait 15-30 minutes and try again.")
                        raise
                else:
                    raise
            except Exception as e:
                logger.error(f"❌ Failed to start bot: {e}")
                raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
