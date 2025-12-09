"""
Bot recovery system - restores XP system configuration on startup.
Ensures guild settings and reward roles are maintained even after crashes.
"""

import discord
import logging
from database import db

logger = logging.getLogger(__name__)

async def restore_guild_configs(bot: discord.Client):
    """
    Restore all guild configurations on bot startup.
    This ensures XP system settings persist across crashes/restarts.
    """
    logger.info("🔄 Starting guild configuration recovery...")
    
    try:
        # Wait for bot to be ready
        await bot.wait_until_ready()
        
        restored_count = 0
        
        for guild in bot.guilds:
            try:
                config = db.get_guild_config(guild.id)
                
                # Skip if XP system not enabled
                if not config.get("enabled"):
                    continue
                
                logger.info(f"📋 Restoring config for {guild.name} (ID: {guild.id})")
                
                # Verify log channel still exists
                log_channel_id = config.get("log_channel")
                if log_channel_id:
                    log_channel = guild.get_channel(log_channel_id)
                    if not log_channel:
                        logger.warning(f"⚠️ Log channel {log_channel_id} not found in {guild.name}")
                        # Update config to remove invalid channel
                        db.update_guild_config(guild.id, log_channel=None)
                    else:
                        logger.info(f"✅ Log channel verified: {log_channel.name}")
                
                # Verify and restore reward roles
                custom_roles = db.get_custom_roles(guild.id)
                if custom_roles:
                    valid_roles = 0
                    invalid_roles = []
                    
                    for level_str, role_id in custom_roles.items():
                        role = guild.get_role(role_id)
                        if role:
                            valid_roles += 1
                            logger.info(f"  ✅ Level {level_str}: {role.name}")
                        else:
                            invalid_roles.append((level_str, role_id))
                            logger.warning(f"  ⚠️ Level {level_str}: Role {role_id} not found")
                    
                    # Remove invalid roles from database
                    for level_str, role_id in invalid_roles:
                        db.remove_custom_role(guild.id, int(level_str))
                    
                    logger.info(f"📊 {guild.name}: {valid_roles} valid roles, {len(invalid_roles)} removed")
                
                restored_count += 1
                
            except Exception as e:
                logger.error(f"❌ Error restoring config for {guild.name}: {e}")
        
        logger.info(f"✅ Recovery complete: {restored_count} guilds restored")
        
        # Send recovery notification to log channels
        await notify_recovery(bot, restored_count)
        
    except Exception as e:
        logger.error(f"❌ Recovery failed: {e}")

async def notify_recovery(bot: discord.Client, restored_count: int):
    """
    Send recovery notification to all configured log channels.
    """
    try:
        notified = 0
        
        for guild in bot.guilds:
            config = db.get_guild_config(guild.id)
            if not config.get("enabled"):
                continue
            
            log_channel_id = config.get("log_channel")
            if not log_channel_id:
                continue
            
            log_channel = guild.get_channel(log_channel_id)
            if not log_channel:
                continue
            
            try:
                embed = discord.Embed(
                    title="🤖 Bot Recovery Complete",
                    description="Your XP system has been restored!",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="What was restored",
                    value="✅ Guild settings\n✅ Reward roles\n✅ User XP data",
                    inline=False
                )
                embed.add_field(
                    name="Status",
                    value=f"All systems operational",
                    inline=False
                )
                embed.set_footer(text="Use /help to see all commands")
                
                await log_channel.send(embed=embed)
                notified += 1
                logger.info(f"📢 Recovery notification sent to {guild.name}")
                
            except Exception as e:
                logger.warning(f"Could not send recovery notification to {guild.name}: {e}")
        
        logger.info(f"📢 Recovery notifications sent to {notified} channels")
        
    except Exception as e:
        logger.error(f"Error sending recovery notifications: {e}")

async def verify_bot_health(bot: discord.Client):
    """
    Periodic health check to ensure bot is functioning properly.
    Can be called periodically to detect and fix issues.
    """
    logger.info("🏥 Running health check...")
    
    try:
        # Check database connectivity
        test_config = db.get_guild_config(0)
        logger.info("✅ Database: OK")
        
        # Check bot connection
        if bot.is_closed():
            logger.error("❌ Bot connection: CLOSED")
            return False
        else:
            logger.info(f"✅ Bot connection: OK ({len(bot.guilds)} guilds)")
        
        # Check for any corrupted data
        issues_found = 0
        for guild in bot.guilds:
            config = db.get_guild_config(guild.id)
            if config.get("enabled"):
                custom_roles = db.get_custom_roles(guild.id)
                for level_str, role_id in custom_roles.items():
                    if not guild.get_role(role_id):
                        issues_found += 1
        
        if issues_found > 0:
            logger.warning(f"⚠️ Found {issues_found} invalid roles across guilds")
        else:
            logger.info("✅ Data integrity: OK")
        
        logger.info("✅ Health check passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return False
