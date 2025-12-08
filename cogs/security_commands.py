import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class SecurityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.security_config = self.load_config()
        
        # Anti-spam tracking
        self.message_tracker = defaultdict(list)
        self.mention_tracker = defaultdict(list)
        self.join_tracker = []
        
    def load_config(self):
        """Load security configuration."""
        if os.path.exists('security_config.json'):
            with open('security_config.json', 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save security configuration."""
        with open('security_config.json', 'w') as f:
            json.dump(self.security_config, f, indent=4)
    
    def get_guild_config(self, guild_id: int):
        """Get configuration for a specific guild."""
        guild_id_str = str(guild_id)
        if guild_id_str not in self.security_config:
            self.security_config[guild_id_str] = {
                "anti_spam": True,
                "anti_raid": True,
                "anti_alt": True,
                "bad_words_enabled": False,
                "verification_enabled": False,
                "logging_enabled": False,
                "log_channel": None,
                "verification_role": None,
                "verification_channel": None,
                "max_mentions": 5,
                "max_messages": 5,
                "message_interval": 5,
                "bad_words": [],
                "raid_max_joins": 10,
                "raid_action": "alert",
                "lockdown_mode": False
            }
            self.save_config()
        return self.security_config[guild_id_str]
    
    @app_commands.command(name="security", description="Configure server security settings.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        feature="Security feature to toggle",
        enabled="Enable or disable"
    )
    @app_commands.choices(feature=[
        app_commands.Choice(name="Anti-Spam Protection", value="anti_spam"),
        app_commands.Choice(name="Anti-Raid Protection", value="anti_raid"),
        app_commands.Choice(name="Anti-Alt Detection", value="anti_alt"),
        app_commands.Choice(name="Bad Words Filter", value="bad_words_enabled"),
        app_commands.Choice(name="Verification System", value="verification_enabled"),
        app_commands.Choice(name="Security Logging", value="logging_enabled")
    ])
    async def security(self, interaction: discord.Interaction, feature: str, enabled: bool):
        config = self.get_guild_config(interaction.guild.id)
        config[feature] = enabled
        self.save_config()
        
        status = "✅ Enabled" if enabled else "❌ Disabled"
        feature_name = feature.replace('_', ' ').title()
        
        embed = discord.Embed(
            title="🛡️ Security Settings Updated",
            description=f"**{feature_name}:** {status}",
            color=discord.Color.green() if enabled else discord.Color.red()
        )
        
        # Add setup instructions if needed
        if enabled:
            if feature == "verification_enabled":
                embed.add_field(
                    name="Next Step",
                    value="Use `/setverify` to configure verification role",
                    inline=False
                )
            elif feature == "logging_enabled":
                embed.add_field(
                    name="Next Step",
                    value="Use `/setlog` to set the log channel",
                    inline=False
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} set {feature} to {enabled} in {interaction.guild}")
    
    @app_commands.command(name="setlog", description="Set the security log channel.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="Channel for security logs")
    async def setlog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = self.get_guild_config(interaction.guild.id)
        config["log_channel"] = channel.id
        config["logging_enabled"] = True
        self.save_config()
        
        embed = discord.Embed(
            title="📝 Log Channel Set",
            description=f"Security logs will be sent to {channel.mention}\n\n"
                       f"Logging has been automatically enabled.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} set log channel to {channel.name} in {interaction.guild}")
    
    @app_commands.command(name="setverify", description="Set up verification system.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        role="Role to give after verification",
        channel="Channel for verification messages"
    )
    async def setverify(self, interaction: discord.Interaction, role: discord.Role, channel: discord.TextChannel = None):
        config = self.get_guild_config(interaction.guild.id)
        config["verification_role"] = role.id
        config["verification_enabled"] = True
        if channel:
            config["verification_channel"] = channel.id
        self.save_config()
        
        embed = discord.Embed(
            title="✅ Verification System Configured",
            description=f"**Verification Role:** {role.mention}\n"
                       f"**Verification Channel:** {channel.mention if channel else 'Not set'}",
            color=discord.Color.green()
        )
        embed.add_field(
            name="How it works",
            value="New members will need to click a button to get verified and receive the role.",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} configured verification in {interaction.guild}")
    
    @app_commands.command(name="verify_panel", description="Send verification panel to a channel.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(channel="Channel to send verification panel")
    async def verify_panel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        config = self.get_guild_config(interaction.guild.id)
        
        if not config.get("verification_enabled"):
            await interaction.response.send_message(
                "❌ Verification system is not enabled. Use `/security verification_enabled true` first.",
                ephemeral=True
            )
            return
        
        if not config.get("verification_role"):
            await interaction.response.send_message(
                "❌ Verification role not set. Use `/setverify` first.",
                ephemeral=True
            )
            return
        
        role = interaction.guild.get_role(config["verification_role"])
        if not role:
            await interaction.response.send_message("❌ Verification role not found.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="✅ Verification Required",
            description=f"Welcome to **{interaction.guild.name}**!\n\n"
                       f"Click the button below to verify and get access to the server.",
            color=discord.Color.green()
        )
        embed.set_footer(text="Click 'Verify' to get started!")
        
        view = VerificationView(role.id)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ Verification panel sent to {channel.mention}", ephemeral=True)
    
    @app_commands.command(name="security_status", description="View current security settings.")
    @app_commands.default_permissions(administrator=True)
    async def security_status(self, interaction: discord.Interaction):
        config = self.get_guild_config(interaction.guild.id)
        
        # Get status emojis
        def status(enabled): return "✅ Enabled" if enabled else "❌ Disabled"
        
        embed = discord.Embed(
            title="🛡️ Security Status",
            description=f"Current security configuration for **{interaction.guild.name}**",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Protection Features",
            value=f"**Anti-Spam:** {status(config.get('anti_spam', True))}\n"
                  f"**Anti-Raid:** {status(config.get('anti_raid', True))}\n"
                  f"**Anti-Alt:** {status(config.get('anti_alt', True))}\n"
                  f"**Bad Words Filter:** {status(config.get('bad_words_enabled', False))}\n"
                  f"**Verification:** {status(config.get('verification_enabled', False))}",
            inline=False
        )
        
        log_channel = interaction.guild.get_channel(config.get("log_channel")) if config.get("log_channel") else None
        verify_role = interaction.guild.get_role(config.get("verification_role")) if config.get("verification_role") else None
        
        embed.add_field(
            name="Configuration",
            value=f"**Log Channel:** {log_channel.mention if log_channel else 'Not set'}\n"
                  f"**Verification Role:** {verify_role.mention if verify_role else 'Not set'}\n"
                  f"**Filtered Words:** {len(config.get('bad_words', []))} words\n"
                  f"**Lockdown Mode:** {status(config.get('lockdown_mode', False))}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="lockdown", description="Lock down the entire server.")
    @app_commands.default_permissions(administrator=True)
    async def lockdown(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        config = self.get_guild_config(interaction.guild.id)
        config["lockdown_mode"] = True
        self.save_config()
        
        locked_count = 0
        for channel in interaction.guild.text_channels:
            try:
                overwrite = channel.overwrites_for(interaction.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                locked_count += 1
            except:
                pass
        
        embed = discord.Embed(
            title="🔒 Server Lockdown Activated",
            description=f"Locked {locked_count} channels. Use `/unlock_server` to restore.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Log to security channel
        await self.log_security_event(
            interaction.guild,
            "🔒 Server Lockdown",
            f"{interaction.user.mention} activated server lockdown",
            discord.Color.red()
        )
    
    @app_commands.command(name="unlock_server", description="Remove server lockdown.")
    @app_commands.default_permissions(administrator=True)
    async def unlock_server(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        config = self.get_guild_config(interaction.guild.id)
        config["lockdown_mode"] = False
        self.save_config()
        
        unlocked_count = 0
        for channel in interaction.guild.text_channels:
            try:
                overwrite = channel.overwrites_for(interaction.guild.default_role)
                overwrite.send_messages = None
                await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
                unlocked_count += 1
            except:
                pass
        
        embed = discord.Embed(
            title="🔓 Server Lockdown Removed",
            description=f"Unlocked {unlocked_count} channels.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        await self.log_security_event(
            interaction.guild,
            "🔓 Lockdown Removed",
            f"{interaction.user.mention} removed server lockdown",
            discord.Color.green()
        )
    
    @app_commands.command(name="backup", description="Create a server backup.")
    @app_commands.default_permissions(administrator=True)
    async def backup(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        guild = interaction.guild
        backup_data = {
            "server_name": guild.name,
            "server_id": guild.id,
            "created_at": datetime.now().isoformat(),
            "roles": [],
            "channels": [],
            "categories": []
        }
        
        # Backup roles
        for role in guild.roles:
            if role.name != "@everyone":
                backup_data["roles"].append({
                    "name": role.name,
                    "color": str(role.color),
                    "permissions": role.permissions.value,
                    "position": role.position,
                    "mentionable": role.mentionable,
                    "hoist": role.hoist
                })
        
        # Backup categories and channels
        for category in guild.categories:
            backup_data["categories"].append({
                "name": category.name,
                "position": category.position
            })
        
        for channel in guild.channels:
            channel_data = {
                "name": channel.name,
                "type": str(channel.type),
                "position": channel.position
            }
            if hasattr(channel, 'category') and channel.category:
                channel_data["category"] = channel.category.name
            backup_data["channels"].append(channel_data)
        
        # Save backup
        filename = f"backup_{guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=4)
        
        embed = discord.Embed(
            title="💾 Server Backup Created",
            description=f"Backup saved as `{filename}`\n\n"
                       f"**Backed up:**\n"
                       f"• {len(backup_data['roles'])} roles\n"
                       f"• {len(backup_data['channels'])} channels\n"
                       f"• {len(backup_data['categories'])} categories",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Backup created for {guild.name} by {interaction.user}")
    
    @app_commands.command(name="antiraid", description="Configure anti-raid settings.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        max_joins="Maximum joins per minute before triggering",
        action="Action to take"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Kick new members", value="kick"),
        app_commands.Choice(name="Ban new members", value="ban"),
        app_commands.Choice(name="Alert only", value="alert")
    ])
    async def antiraid(self, interaction: discord.Interaction, max_joins: int, action: str):
        config = self.get_guild_config(interaction.guild.id)
        config["raid_max_joins"] = max_joins
        config["raid_action"] = action
        self.save_config()
        
        embed = discord.Embed(
            title="🛡️ Anti-Raid Configured",
            description=f"**Max joins per minute:** {max_joins}\n**Action:** {action.title()}",
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="badwords", description="Manage bad words filter.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        action="Add or remove word",
        word="Word to filter"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Remove", value="remove"),
        app_commands.Choice(name="List", value="list")
    ])
    async def badwords(self, interaction: discord.Interaction, action: str, word: str = None):
        config = self.get_guild_config(interaction.guild.id)
        
        if action == "list":
            words = config.get("bad_words", [])
            embed = discord.Embed(
                title="📝 Filtered Words",
                description=", ".join(words) if words else "No words filtered",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if not word:
            await interaction.response.send_message("❌ Please provide a word.", ephemeral=True)
            return
        
        word = word.lower()
        if action == "add":
            if word not in config["bad_words"]:
                config["bad_words"].append(word)
                self.save_config()
                await interaction.response.send_message(f"✅ Added `{word}` to filter.", ephemeral=True)
            else:
                await interaction.response.send_message(f"⚠️ `{word}` is already filtered.", ephemeral=True)
        elif action == "remove":
            if word in config["bad_words"]:
                config["bad_words"].remove(word)
                self.save_config()
                await interaction.response.send_message(f"✅ Removed `{word}` from filter.", ephemeral=True)
            else:
                await interaction.response.send_message(f"⚠️ `{word}` is not in filter.", ephemeral=True)
    
    async def log_security_event(self, guild, title, description, color):
        """Log security events to the configured channel."""
        config = self.get_guild_config(guild.id)
        
        # Check if logging is enabled
        if not config.get("logging_enabled", False):
            return
        
        log_channel_id = config.get("log_channel")
        
        if log_channel_id:
            channel = guild.get_channel(log_channel_id)
            if channel:
                embed = discord.Embed(
                    title=title,
                    description=description,
                    color=color,
                    timestamp=datetime.now()
                )
                try:
                    await channel.send(embed=embed)
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Monitor messages for spam and bad words."""
        if message.author.bot or not message.guild:
            return
        
        config = self.get_guild_config(message.guild.id)
        
        # Check bad words (only if enabled)
        if config.get("bad_words_enabled", False) and config.get("bad_words"):
            content_lower = message.content.lower()
            for word in config["bad_words"]:
                if word in content_lower:
                    try:
                        await message.delete()
                        await message.channel.send(
                            f"{message.author.mention} Please watch your language!",
                            delete_after=5
                        )
                        await self.log_security_event(
                            message.guild,
                            "🚫 Bad Word Detected",
                            f"{message.author.mention} used filtered word in {message.channel.mention}",
                            discord.Color.orange()
                        )
                    except:
                        pass
                    return
        
        # Anti-spam check
        if config.get("anti_spam"):
            user_id = message.author.id
            now = datetime.now()
            
            # Track messages
            self.message_tracker[user_id].append(now)
            self.message_tracker[user_id] = [
                t for t in self.message_tracker[user_id]
                if now - t < timedelta(seconds=config.get("message_interval", 5))
            ]
            
            # Check if spamming
            if len(self.message_tracker[user_id]) > config.get("max_messages", 5):
                try:
                    await message.author.timeout(timedelta(minutes=5), reason="Spam detected")
                    await message.channel.send(
                        f"{message.author.mention} has been timed out for spamming.",
                        delete_after=10
                    )
                    await self.log_security_event(
                        message.guild,
                        "⚠️ Spam Detected",
                        f"{message.author.mention} was timed out for spamming in {message.channel.mention}",
                        discord.Color.red()
                    )
                    self.message_tracker[user_id].clear()
                except:
                    pass
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Monitor member joins for raids and alt accounts."""
        config = self.get_guild_config(member.guild.id)
        
        # Anti-alt detection
        if config.get("anti_alt"):
            account_age = datetime.now() - member.created_at.replace(tzinfo=None)
            if account_age < timedelta(days=7):
                await self.log_security_event(
                    member.guild,
                    "⚠️ Suspicious Account",
                    f"{member.mention} joined with account age: {account_age.days} days",
                    discord.Color.yellow()
                )
        
        # Anti-raid detection
        if config.get("anti_raid"):
            now = datetime.now()
            self.join_tracker.append(now)
            self.join_tracker = [t for t in self.join_tracker if now - t < timedelta(minutes=1)]
            
            max_joins = config.get("raid_max_joins", 10)
            if len(self.join_tracker) > max_joins:
                await self.log_security_event(
                    member.guild,
                    "🚨 RAID DETECTED",
                    f"More than {max_joins} joins in 1 minute! Consider using `/lockdown`",
                    discord.Color.dark_red()
                )

class VerificationView(discord.ui.View):
    """Persistent view for verification button."""
    def __init__(self, role_id: int):
        super().__init__(timeout=None)
        self.role_id = role_id
    
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.role_id)
        
        if not role:
            await interaction.response.send_message("❌ Verification role not found.", ephemeral=True)
            return
        
        if role in interaction.user.roles:
            await interaction.response.send_message("✅ You are already verified!", ephemeral=True)
            return
        
        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Welcome! You have been verified and received the {role.mention} role!",
                ephemeral=True
            )
            logger.info(f"{interaction.user} verified in {interaction.guild}")
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Failed to verify: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(SecurityCommands(bot))
