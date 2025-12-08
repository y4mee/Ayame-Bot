import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import random
from database import db

logger = logging.getLogger(__name__)

# Role themes for auto-generation
ROLE_THEMES = {
    "anime": [
        {"level": 1, "name": "🌸 Sakura Seed", "color": 0xFFB7C5},
        {"level": 5, "name": "🌱 Petal Sprout", "color": 0xFFD4E5},
        {"level": 10, "name": "🌺 Cherry Whisper", "color": 0xFF69B4},
        {"level": 15, "name": "☁️ Cloud Drifter", "color": 0xB0E0E6},
        {"level": 20, "name": "🦋 Kawaii Walker", "color": 0xDDA0DD},
        {"level": 25, "name": "💎 Yugen Soul", "color": 0x9370DB},
        {"level": 30, "name": "🌸 Petal Knight", "color": 0xFF1493},
        {"level": 40, "name": "🌙 Moonlit Mystic", "color": 0x4169E1},
        {"level": 50, "name": "🦋 Dreambound Spirit", "color": 0x8A2BE2},
        {"level": 75, "name": "💠 Celestial Kimono", "color": 0x00CED1},
        {"level": 100, "name": "⭐ Orb Ascendant", "color": 0xFFD700}
    ],
    "gaming": [
        {"level": 1, "name": "🎮 Noob", "color": 0x808080},
        {"level": 5, "name": "🕹️ Casual Player", "color": 0x90EE90},
        {"level": 10, "name": "🎯 Skilled Gamer", "color": 0x87CEEB},
        {"level": 15, "name": "⚡ Pro Player", "color": 0x9370DB},
        {"level": 20, "name": "🔥 Elite Gamer", "color": 0xFF6347},
        {"level": 25, "name": "💪 Veteran", "color": 0xFF8C00},
        {"level": 30, "name": "🏆 Champion", "color": 0xFFD700},
        {"level": 40, "name": "👑 Master", "color": 0xFF1493},
        {"level": 50, "name": "💎 Grandmaster", "color": 0x00CED1},
        {"level": 75, "name": "🌟 Legend", "color": 0x9400D3},
        {"level": 100, "name": "🔱 Mythic", "color": 0xFF0000}
    ],
    "ranks": [
        {"level": 1, "name": "🥉 Bronze I", "color": 0xCD7F32},
        {"level": 5, "name": "🥉 Bronze II", "color": 0xD4915D},
        {"level": 10, "name": "🥉 Bronze III", "color": 0xE0A875},
        {"level": 15, "name": "🥈 Silver I", "color": 0xC0C0C0},
        {"level": 20, "name": "🥈 Silver II", "color": 0xD3D3D3},
        {"level": 25, "name": "🥈 Silver III", "color": 0xE8E8E8},
        {"level": 30, "name": "🥇 Gold I", "color": 0xFFD700},
        {"level": 40, "name": "🥇 Gold II", "color": 0xFFE55C},
        {"level": 50, "name": "💎 Platinum", "color": 0xE5E4E2},
        {"level": 75, "name": "💠 Diamond", "color": 0xB9F2FF},
        {"level": 100, "name": "👑 Master", "color": 0xFF0080}
    ],
    "fantasy": [
        {"level": 1, "name": "🌱 Peasant", "color": 0x8B4513},
        {"level": 5, "name": "⚔️ Squire", "color": 0xA0522D},
        {"level": 10, "name": "🗡️ Knight", "color": 0xC0C0C0},
        {"level": 15, "name": "🛡️ Paladin", "color": 0xFFD700},
        {"level": 20, "name": "🏹 Ranger", "color": 0x228B22},
        {"level": 25, "name": "🔮 Mage", "color": 0x9370DB},
        {"level": 30, "name": "⚡ Sorcerer", "color": 0x4169E1},
        {"level": 40, "name": "🌟 Archmage", "color": 0xFF1493},
        {"level": 50, "name": "🐉 Dragon Slayer", "color": 0xFF4500},
        {"level": 75, "name": "👑 King", "color": 0xFFD700},
        {"level": 100, "name": "🔱 God", "color": 0xFF0000}
    ],
    "space": [
        {"level": 1, "name": "🌍 Earthling", "color": 0x87CEEB},
        {"level": 5, "name": "🚀 Cadet", "color": 0x4682B4},
        {"level": 10, "name": "🛸 Pilot", "color": 0x6495ED},
        {"level": 15, "name": "⭐ Navigator", "color": 0x9370DB},
        {"level": 20, "name": "🌙 Explorer", "color": 0xC0C0C0},
        {"level": 25, "name": "🪐 Commander", "color": 0xFF8C00},
        {"level": 30, "name": "☄️ Captain", "color": 0xFFD700},
        {"level": 40, "name": "🌟 Admiral", "color": 0xFF1493},
        {"level": 50, "name": "🌌 Cosmic Voyager", "color": 0x9400D3},
        {"level": 75, "name": "✨ Starlord", "color": 0x00CED1},
        {"level": 100, "name": "🌠 Celestial Being", "color": 0xFF0080}
    ],
    "simple": [
        {"level": 1, "name": "Level 1", "color": 0xFFB7C5},
        {"level": 5, "name": "Level 5", "color": 0xFFD4E5},
        {"level": 10, "name": "Level 10", "color": 0xFF69B4},
        {"level": 15, "name": "Level 15", "color": 0xB0E0E6},
        {"level": 20, "name": "Level 20", "color": 0xDDA0DD},
        {"level": 25, "name": "Level 25", "color": 0x9370DB},
        {"level": 30, "name": "Level 30", "color": 0xFF1493},
        {"level": 40, "name": "Level 40", "color": 0x4169E1},
        {"level": 50, "name": "Level 50", "color": 0x8A2BE2},
        {"level": 75, "name": "Level 75", "color": 0x00CED1},
        {"level": 100, "name": "Level 100", "color": 0xFFD700}
    ]
}

# XP ranges for different activities (per hour) - random value in range
ACTIVITY_XP_RANGES = {
    "listening": (3, 8),      # Spotify, music - 3-8 XP per hour
    "playing": (8, 15),       # Games, apps - 8-15 XP per hour
    "streaming": (12, 20),    # Streaming - 12-20 XP per hour
    "watching": (5, 10),      # Watching - 5-10 XP per hour
    "competing": (10, 18),    # Competing in games - 10-18 XP per hour
    "unknown": (3, 7)         # Unknown activities - 3-7 XP per hour
}

class ActivityXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_activity = defaultdict(dict)
        self.cooldowns = defaultdict(lambda: datetime.now() - timedelta(hours=2))
        self.streaks = defaultdict(lambda: {"count": 0, "activity": None, "last_time": None})
    
    def get_guild_config(self, guild_id: int):
        """Get configuration for a specific guild."""
        config = db.get_guild_config(guild_id)
        # Add custom_roles from database
        config["custom_roles"] = db.get_custom_roles(guild_id)
        return config
    
    def get_user_xp(self, guild_id: int, user_id: int):
        """Get XP for a user in a guild."""
        return db.get_user_xp(guild_id, user_id)
    
    def add_xp(self, guild_id: int, user_id: int, amount: int):
        """Add XP to a user."""
        return db.add_xp(guild_id, user_id, amount)
    
    def get_role_for_level(self, guild_id: int, level: int):
        """Get the appropriate role for a level from custom roles."""
        custom_roles = db.get_custom_roles(guild_id)
        
        # Find the highest level role that user qualifies for
        appropriate_level = None
        for role_level in sorted([int(l) for l in custom_roles.keys()], reverse=True):
            if level >= role_level:
                appropriate_level = role_level
                break
        
        if appropriate_level:
            return {"level": appropriate_level, "role_id": custom_roles[str(appropriate_level)]}
        return None
    
    @app_commands.command(name="setxpsystem", description="Setup activity XP system.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        channel="Channel for XP logs and commands",
        create_roles="Create automatic reward roles?",
        theme="[Only if create_roles=True] Choose theme for roles"
    )
    @app_commands.choices(
        theme=[
            app_commands.Choice(name="🌸 Anime", value="anime"),
            app_commands.Choice(name="🎮 Gaming", value="gaming"),
            app_commands.Choice(name="🏆 Ranks", value="ranks")
        ]
    )
    async def setxpsystem(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        create_roles: bool = False,
        theme: str = "anime"
    ):
        """Setup XP system with optional automatic role creation."""
        await interaction.response.defer(ephemeral=True)
        
        # Save configuration
        db.update_guild_config(
            interaction.guild.id,
            enabled=True,
            log_channel=channel.id,
            target_role=None,  # Track everyone
            auto_roles=create_roles
        )
        
        embed = discord.Embed(
            title="✅ XP System Setup",
            description="Activity XP tracking is now active!",
            color=0x5865F2
        )
        embed.add_field(name="Log Channel", value=channel.mention, inline=True)
        embed.add_field(name="Auto Roles", value="✅ Yes" if create_roles else "❌ No", inline=True)
        
        # Create themed roles if requested
        if create_roles:
            theme_roles = ROLE_THEMES.get(theme, ROLE_THEMES["anime"])
            created = []
            
            for role_data in theme_roles:
                try:
                    new_role = await interaction.guild.create_role(
                        name=role_data["name"],
                        color=discord.Color(role_data["color"]),
                        reason=f"XP reward role - {theme} theme"
                    )
                    db.add_custom_role(interaction.guild.id, role_data["level"], new_role.id)
                    created.append(f"Lv.{role_data['level']} → {new_role.mention}")
                except Exception as e:
                    logger.error(f"Failed to create role: {e}")
            
            if created:
                roles_text = "\n".join(created[:5])
                if len(created) > 5:
                    roles_text += f"\n*+{len(created) - 5} more*"
                embed.add_field(name=f"{theme.title()} Roles Created", value=roles_text, inline=False)
        else:
            embed.add_field(
                name="Manual Setup",
                value="Use `/setrewardrole <level> @role` to add rewards",
                inline=False
            )
        
        embed.add_field(
            name="How It Works",
            value="Users earn XP by being active (Spotify, gaming, etc.)\n"
                  "Check progress with `/xp`, `/rank`, `/leaderboard`",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} setup XP system: roles={create_roles}, theme={theme}")
    
    @app_commands.command(name="setrewardrole", description="Set reward role for a level and sync to all users.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        level="Level required for this role",
        role="Role to assign"
    )
    async def setrewardrole(self, interaction: discord.Interaction, level: int, role: discord.Role):
        """Set a reward role and immediately sync it to all qualifying users."""
        await interaction.response.defer(ephemeral=True)
        
        if level < 1:
            await interaction.followup.send("❌ Level must be 1 or higher!", ephemeral=True)
            return
        
        # Check if bot can manage this role
        if role >= interaction.guild.me.top_role:
            await interaction.followup.send("❌ I cannot manage this role (it's higher than my highest role)!", ephemeral=True)
            return
        
        # Add role to reward system
        db.add_custom_role(interaction.guild.id, level, role.id)
        
        # Auto-sync: Give role to all users at this level or higher
        guild_id = interaction.guild.id
        leaderboard_data = db.get_leaderboard(guild_id, limit=10000)
        
        synced = 0
        skipped = 0
        
        for user_id, xp, user_level in leaderboard_data:
            if user_level < level:
                continue
                
            member = interaction.guild.get_member(user_id)
            if not member:
                continue
            
            if role in member.roles:
                skipped += 1
                continue
            
            try:
                await member.add_roles(role, reason=f"Reward role for Level {level}")
                synced += 1
            except Exception as e:
                logger.error(f"Failed to assign role to {member.name}: {e}")
        
        embed = discord.Embed(
            title="✅ Reward Role Set",
            description=f"Level **{level}** → {role.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Synced", value=f"{synced} users got the role", inline=True)
        if skipped > 0:
            embed.add_field(name="Skipped", value=f"{skipped} already had it", inline=True)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} set reward role: Level {level} → {role.name}, synced to {synced} users")
    
    @app_commands.command(name="editrewardrole", description="Change reward role for a level.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        level="Level to edit",
        newrole="New role to assign"
    )
    async def editrewardrole(self, interaction: discord.Interaction, level: int, newrole: discord.Role):
        """Edit an existing reward role and sync changes."""
        await interaction.response.defer(ephemeral=True)
        
        guild_id = interaction.guild.id
        custom_roles = db.get_custom_roles(guild_id)
        
        # Check if level exists
        if str(level) not in custom_roles:
            await interaction.followup.send(f"❌ No reward role set for Level {level}!", ephemeral=True)
            return
        
        # Check if bot can manage new role
        if newrole >= interaction.guild.me.top_role:
            await interaction.followup.send("❌ I cannot manage this role (it's higher than my highest role)!", ephemeral=True)
            return
        
        old_role_id = custom_roles[str(level)]
        old_role = interaction.guild.get_role(old_role_id)
        
        # Update role in database
        db.add_custom_role(guild_id, level, newrole.id)
        
        # Sync: Remove old role and add new role to qualifying users
        leaderboard_data = db.get_leaderboard(guild_id, limit=10000)
        
        updated = 0
        
        for user_id, xp, user_level in leaderboard_data:
            if user_level < level:
                continue
            
            member = interaction.guild.get_member(user_id)
            if not member:
                continue
            
            try:
                # Remove old role if they have it
                if old_role and old_role in member.roles:
                    await member.remove_roles(old_role, reason=f"Reward role changed for Level {level}")
                
                # Add new role if they don't have it
                if newrole not in member.roles:
                    await member.add_roles(newrole, reason=f"Updated reward role for Level {level}")
                    updated += 1
            except Exception as e:
                logger.error(f"Failed to update role for {member.name}: {e}")
        
        embed = discord.Embed(
            title="✅ Reward Role Updated",
            description=f"Level **{level}**\n{old_role.mention if old_role else 'Old role'} → {newrole.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Users Updated", value=str(updated), inline=True)
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user} edited reward role: Level {level} → {newrole.name}, updated {updated} users")
    

    @app_commands.command(name="xp", description="Check your XP and level.")
    @app_commands.describe(member="Member to check (optional)")
    async def xp(self, interaction: discord.Interaction, member: discord.Member = None):
        # Check if XP system is configured
        config = self.get_guild_config(interaction.guild.id)
        if not config.get("enabled"):
            await interaction.response.send_message(
                "❌ Activity XP system is not configured in this server.\n"
                "Ask an admin to run `/activityxp` to set it up!",
                ephemeral=True
            )
            return
        
        # Check if command is used in log channel
        log_channel_id = config.get("log_channel")
        if log_channel_id and interaction.channel.id != log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await interaction.response.send_message(
                f"❌ XP commands can only be used in {log_channel.mention}!",
                ephemeral=True
            )
            return
        
        target = member or interaction.user
        data = self.get_user_xp(interaction.guild.id, target.id)
        
        # Get custom roles for this server
        custom_roles = db.get_custom_roles(interaction.guild.id)
        
        current_role_info = self.get_role_for_level(interaction.guild.id, data["level"])
        next_role_info = None
        
        # Find next role
        for level in sorted([int(l) for l in custom_roles.keys()]):
            if level > data["level"]:
                next_role_info = {"level": level, "role_id": custom_roles[str(level)]}
                break
        
        # Clean, minimal XP card
        embed = discord.Embed(
            description=f"**{target.display_name}**",
            color=0x5865F2
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        
        # Main stats in one line
        embed.add_field(name="Level", value=f"`{data['level']}`", inline=True)
        embed.add_field(name="XP", value=f"`{data['xp']}`", inline=True)
        embed.add_field(name="Next", value=f"`{100 - (data['xp'] % 100)}`", inline=True)
        
        # Roles if available
        if current_role_info:
            role = interaction.guild.get_role(current_role_info["role_id"])
            if role:
                embed.add_field(name="Role", value=role.mention, inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View XP leaderboard.")
    @app_commands.describe(page="Page number (default: 1)")
    async def leaderboard(self, interaction: discord.Interaction, page: int = 1):
        # Check if XP system is configured
        config = self.get_guild_config(interaction.guild.id)
        if not config.get("enabled"):
            await interaction.response.send_message(
                "❌ Activity XP system is not configured in this server.\n"
                "Ask an admin to run `/activityxp` to set it up!",
                ephemeral=True
            )
            return
        
        # Check if command is used in log channel
        log_channel_id = config.get("log_channel")
        if log_channel_id and interaction.channel.id != log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await interaction.response.send_message(
                f"❌ XP commands can only be used in {log_channel.mention}!",
                ephemeral=True
            )
            return
        
        guild_id = interaction.guild.id
        
        # Get all users in this guild from database
        leaderboard_data = db.get_leaderboard(guild_id, limit=1000)
        guild_users = []
        for user_id, xp, level in leaderboard_data:
            member = interaction.guild.get_member(user_id)
            if member:
                guild_users.append((member, xp, level))
        
        if not guild_users:
            await interaction.response.send_message("❌ No users with XP yet!", ephemeral=True)
            return
        
        # Sort by XP
        guild_users.sort(key=lambda x: x[1], reverse=True)
        
        # Pagination
        per_page = 10
        total_pages = (len(guild_users) + per_page - 1) // per_page
        page = max(1, min(page, total_pages))
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        page_users = guild_users[start_idx:end_idx]
        
        # Clean leaderboard
        embed = discord.Embed(
            title="Leaderboard",
            color=0xFEE75C
        )
        
        # Find user's rank
        user_rank = None
        for i, (member, _, _) in enumerate(guild_users, 1):
            if member.id == interaction.user.id:
                user_rank = i
                break
        
        # Get custom roles for role display
        custom_roles = db.get_custom_roles(guild_id)
        
        leaderboard_text = ""
        for i, (member, xp, level) in enumerate(page_users, start_idx + 1):
            # Medal for top 3
            if i == 1:
                medal = "🥇"
            elif i == 2:
                medal = "🥈"
            elif i == 3:
                medal = "🥉"
            else:
                medal = f"`{i:02d}`"
            
            # Get user's reward role
            role_info = self.get_role_for_level(guild_id, level)
            role_display = ""
            if role_info:
                role = interaction.guild.get_role(role_info["role_id"])
                if role:
                    role_display = f" • {role.mention}"
            
            # Highlight current user
            if member.id == interaction.user.id:
                leaderboard_text += f"{medal} **{member.display_name}** • Lv.{level} • {xp:,} XP{role_display}\n"
            else:
                leaderboard_text += f"{medal} {member.display_name} • Lv.{level} • {xp:,} XP{role_display}\n"
        
        embed.description = leaderboard_text
        
        # Footer with user's rank and pagination
        footer_text = f"Page {page}/{total_pages} • {len(guild_users)} total members"
        if user_rank:
            footer_text += f" • Your rank: #{user_rank}"
        embed.set_footer(text=footer_text)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rank", description="View your rank and detailed stats.")
    @app_commands.describe(member="Member to check (optional)")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        # Check if XP system is configured
        config = self.get_guild_config(interaction.guild.id)
        if not config.get("enabled"):
            await interaction.response.send_message(
                "❌ Activity XP system is not configured in this server.\n"
                "Ask an admin to run `/activityxp` to set it up!",
                ephemeral=True
            )
            return
        
        # Check if command is used in log channel
        log_channel_id = config.get("log_channel")
        if log_channel_id and interaction.channel.id != log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await interaction.response.send_message(
                f"❌ XP commands can only be used in {log_channel.mention}!",
                ephemeral=True
            )
            return
        
        target = member or interaction.user
        guild_id = interaction.guild.id
        
        # Get user data
        data = self.get_user_xp(guild_id, target.id)
        
        # Get all users for ranking from database
        leaderboard_data = db.get_leaderboard(guild_id, limit=1000)
        guild_users = []
        for user_id, xp, _ in leaderboard_data:
            guild_member = interaction.guild.get_member(user_id)
            if guild_member:
                guild_users.append((guild_member, xp))
        
        # Sort and find rank
        guild_users.sort(key=lambda x: x[1], reverse=True)
        rank = None
        for i, (m, _) in enumerate(guild_users, 1):
            if m.id == target.id:
                rank = i
                break
        
        # Get role info
        custom_roles = db.get_custom_roles(guild_id)
        current_role_info = self.get_role_for_level(guild_id, data["level"])
        next_role_info = None
        
        # Find next role
        for level in sorted([int(l) for l in custom_roles.keys()]):
            if level > data["level"]:
                next_role_info = {"level": level, "role_id": custom_roles[str(level)]}
                break
        
        # Calculate progress to next level
        current_level_xp = data["level"] * 100
        next_level_xp = (data["level"] + 1) * 100
        xp_in_level = data["xp"] - current_level_xp
        xp_needed = next_level_xp - data["xp"]
        progress_percent = (xp_in_level / 100) * 100
        
        # Create progress bar
        filled = int(progress_percent / 10)
        empty = 10 - filled
        progress_bar = "█" * filled + "░" * empty
        
        # Clean, minimal rank card
        rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else ""
        
        embed = discord.Embed(
            title=f"{rank_emoji} {target.display_name}",
            description=f"Rank **#{rank}** • Level **{data['level']}** • {data['xp']:,} XP",
            color=0x5865F2
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        
        # Progress bar
        embed.add_field(
            name=f"Progress to Level {data['level'] + 1}",
            value=f"{progress_bar} `{progress_percent:.0f}%`\n{xp_in_level}/{100} XP",
            inline=False
        )
        
        # Show current reward role if user has one
        if current_role_info:
            role = interaction.guild.get_role(current_role_info["role_id"])
            if role:
                embed.add_field(
                    name="Reward Role",
                    value=f"{role.mention}",
                    inline=True
                )
        
        # Show next reward role if available
        if next_role_info:
            next_role = interaction.guild.get_role(next_role_info["role_id"])
            if next_role:
                embed.add_field(
                    name="Next Role",
                    value=f"{next_role.mention} • Lv.{next_role_info['level']}",
                    inline=True
                )
        
        embed.set_footer(text=f"Keep being active to earn more XP!")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="top", description="View top members by category.")
    @app_commands.describe(
        category="What to rank by"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="🏆 Total XP", value="xp"),
        app_commands.Choice(name="⭐ Highest Level", value="level"),
        app_commands.Choice(name="🔥 Current Streaks", value="streak")
    ])
    async def top(self, interaction: discord.Interaction, category: str):
        # Check if XP system is configured
        config = self.get_guild_config(interaction.guild.id)
        if not config.get("enabled"):
            await interaction.response.send_message(
                "❌ Activity XP system is not configured in this server.\n"
                "Ask an admin to run `/activityxp` to set it up!",
                ephemeral=True
            )
            return
        
        # Check if command is used in log channel
        log_channel_id = config.get("log_channel")
        if log_channel_id and interaction.channel.id != log_channel_id:
            log_channel = interaction.guild.get_channel(log_channel_id)
            await interaction.response.send_message(
                f"❌ XP commands can only be used in {log_channel.mention}!",
                ephemeral=True
            )
            return
        
        guild_id = interaction.guild.id
        
        if category == "streak":
            # Get users with active streaks from database
            streak_data = db.get_top_streaks(guild_id, limit=100)
            streak_users = []
            for user_id, activity_name, streak_count in streak_data:
                # Filter out custom status entries
                if activity_name and "Custom:" in activity_name:
                    continue  # Skip custom status
                
                member = interaction.guild.get_member(user_id)
                if member:
                    streak_users.append((member, streak_count, activity_name))
            
            if not streak_users:
                await interaction.response.send_message("❌ No active streaks!", ephemeral=True)
                return
            
            streak_users.sort(key=lambda x: x[1], reverse=True)
            
            # Clean, minimal design
            embed = discord.Embed(
                title="Top Streaks",
                description="Longest activity streaks",
                color=0xFEE75C
            )
            
            streak_text = ""
            for i, (member, count, activity) in enumerate(streak_users[:10], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"`{i:02d}`"
                # Clean activity name
                activity_display = activity.replace("Spotify:", "🎵").replace("Game:", "🎮").replace("Playing:", "🎮").replace("Streaming:", "📺")
                streak_text += f"{medal} **{member.display_name}** • {count}h • {activity_display}\n"
            
            embed.description = streak_text
        
        else:
            # Get all users from database
            leaderboard_data = db.get_leaderboard(guild_id, limit=1000)
            guild_users = []
            for user_id, xp, level in leaderboard_data:
                member = interaction.guild.get_member(user_id)
                if member:
                    guild_users.append((member, xp, level))
            
            if not guild_users:
                await interaction.response.send_message("❌ No users with XP yet!", ephemeral=True)
                return
            
            # Sort by category
            if category == "xp":
                guild_users.sort(key=lambda x: x[1], reverse=True)
                title = "Top XP"
            else:  # level
                guild_users.sort(key=lambda x: x[2], reverse=True)
                title = "Top Levels"
            
            embed = discord.Embed(
                title=title,
                color=0xFEE75C
            )
            
            top_text = ""
            for i, (member, xp, level) in enumerate(guild_users[:10], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"`{i:02d}`"
                
                if category == "xp":
                    top_text += f"{medal} **{member.display_name}** • Lv.{level} • {xp:,} XP\n"
                else:
                    top_text += f"{medal} **{member.display_name}** • Lv.{level} • {xp:,} XP\n"
            
            embed.description = top_text
        
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """Monitor user activity changes."""
        # Debug logging
        logger.info(f"Presence update detected for {after.name}")
        
        if after.bot:
            logger.info(f"Skipping bot: {after.name}")
            return
        
        guild = after.guild
        config = self.get_guild_config(guild.id)
        
        logger.info(f"Config for {guild.name}: enabled={config.get('enabled')}, channel={config.get('log_channel')}")
        
        if not config.get("enabled"):
            logger.info(f"Activity XP not enabled for {guild.name}")
            return
        
        log_channel_id = config.get("log_channel")
        if not log_channel_id:
            logger.info(f"No log channel set for {guild.name}")
            return
        
        log_channel = guild.get_channel(log_channel_id)
        if not log_channel:
            logger.info(f"Log channel {log_channel_id} not found in {guild.name}")
            return
        
        # Check if user has target role (if specified)
        target_role_id = config.get("target_role")
        if target_role_id:
            target_role = guild.get_role(target_role_id)
            if target_role and target_role not in after.roles:
                logger.info(f"{after.name} doesn't have target role")
                return
        
        logger.info(f"{after.name} has {len(after.activities)} activities")
        
        # Detect ANY activity automatically
        user_key = f"{guild.id}_{after.id}"
        activity_detected = None
        xp_range = None
        activity_name = None
        activity_type_key = None
        
        # Check all activities and pick the highest priority one
        # Priority: Streaming > Listening (Spotify) > Playing/Competing > Watching > Custom
        selected_activity = None
        priority = 999
        
        for activity in after.activities:
            logger.info(f"Activity type: {type(activity).__name__}, Activity: {activity}")
            
            current_priority = 999
            
            # Spotify (Listening)
            if isinstance(activity, discord.Spotify):
                current_priority = 2
                if current_priority < priority:
                    priority = current_priority
                    selected_activity = activity
                    activity_type_key = "listening"
                    # Use generic "Spotify" instead of song name to avoid logging every song change
                    activity_name = "Spotify"
                    activity_detected = f"🎵 listening to **{activity.title}** by {activity.artist}"
            
            # Streaming
            elif isinstance(activity, discord.Streaming):
                current_priority = 1
                if current_priority < priority:
                    priority = current_priority
                    selected_activity = activity
                    activity_type_key = "streaming"
                    activity_name = f"Streaming: {activity.name}"
                    activity_detected = f"📺 streaming **{activity.name}**"
            
            # Skip Custom Activity - don't track custom status
            elif isinstance(activity, discord.CustomActivity):
                continue  # Ignore custom status
            
            # All other activities (Games, Apps, etc.)
            elif isinstance(activity, (discord.Activity, discord.Game)):
                # Determine activity type from Discord's ActivityType
                if hasattr(activity, 'type'):
                    if activity.type == discord.ActivityType.playing:
                        current_priority = 3
                        activity_type_key = "playing"
                        emoji = "🎮"
                        verb = "playing"
                    elif activity.type == discord.ActivityType.watching:
                        current_priority = 5
                        activity_type_key = "watching"
                        emoji = "📺"
                        verb = "watching"
                    elif activity.type == discord.ActivityType.listening:
                        current_priority = 2
                        activity_type_key = "listening"
                        emoji = "🎵"
                        verb = "listening to"
                    elif activity.type == discord.ActivityType.competing:
                        current_priority = 4
                        activity_type_key = "competing"
                        emoji = "🏆"
                        verb = "competing in"
                    else:
                        current_priority = 7
                        activity_type_key = "unknown"
                        emoji = "✨"
                        verb = "doing"
                else:
                    # Default to playing for Game type
                    current_priority = 3
                    activity_type_key = "playing"
                    emoji = "🎮"
                    verb = "playing"
                
                if current_priority < priority:
                    priority = current_priority
                    selected_activity = activity
                    activity_name = f"{activity_type_key.title()}: {activity.name}"
                    activity_detected = f"{emoji} {verb} **{activity.name}**"
        
        # Get XP range for the activity type
        if activity_type_key:
            xp_range = ACTIVITY_XP_RANGES.get(activity_type_key, ACTIVITY_XP_RANGES["unknown"])
        
        logger.info(f"Activity detected: {activity_detected}, XP range: {xp_range}")
        
        # If no activity detected, user might have stopped activity
        if not activity_detected or not xp_range:
            # Check if user had activity before and now stopped
            if self.last_activity[user_key].get("current"):
                logger.info(f"{after.name} stopped activity: {self.last_activity[user_key].get('current')}")
                self.last_activity[user_key]["current"] = None
            return
        
        # Check if this is a NEW activity or continuation
        last_logged_activity = self.last_activity[user_key].get("current")
        is_new_activity = (last_logged_activity != activity_name)
        
        # Update last activity
        self.last_activity[user_key]["current"] = activity_name
        
        # Check for streak from database
        streak_data = db.get_streak(guild.id, after.id)
        
        # Check cooldown for XP (1 hour)
        user_data = db.get_user_xp(guild.id, after.id)
        can_earn_xp = True
        
        if user_data.get("last_xp_time"):
            try:
                last_time = datetime.fromisoformat(user_data["last_xp_time"])
                time_since_last = datetime.now() - last_time
                if time_since_last < timedelta(hours=1):
                    can_earn_xp = False
            except:
                pass
        
        # For NEW activity, always log immediately (no XP)
        if is_new_activity:
            # Fixed-width embed with consistent formatting
            embed = discord.Embed(
                description=f"{after.mention} {activity_detected}\n\n"
                           f"XP awarded after 1 hour of activity",
                color=0x5865F2
            )
            
            try:
                await log_channel.send(embed=embed)
                logger.info(f"New activity logged for {after.name}: {activity_detected}")
            except Exception as e:
                logger.error(f"Failed to send activity log: {e}")
            
            # Update streak to 1 (new activity)
            db.update_streak(guild.id, after.id, activity_name, 1)
            return
        
        # For SAME activity, check if we can award XP (1 hour passed)
        if not can_earn_xp:
            logger.info(f"{after.name} continuing same activity, on cooldown")
            return
        
        # Award XP with streak bonus (2x per hour)
        streak_hours = streak_data["count"] + 1
        streak_multiplier = 1.0 + (1.0 * (streak_hours - 1))  # 2x per hour: 1x, 2x, 3x, 4x...
        
        # Generate random XP from range
        base_xp = random.randint(xp_range[0], xp_range[1])
        final_xp = int(base_xp * streak_multiplier)
        
        # Update streak
        db.update_streak(guild.id, after.id, activity_name, streak_hours)
        
        # Add XP
        leveled_up, new_level = self.add_xp(guild.id, after.id, final_xp)
        
        # Send log message with XP - Fixed width format
        user_data = self.get_user_xp(guild.id, after.id)
        
        if streak_hours > 1:
            # Streak message with fixed width
            embed = discord.Embed(
                description=f"{after.mention} • **{streak_hours}h streak**\n\n"
                           f"`XP:` +{final_xp} • `Total:` {user_data['xp']} • `Level:` {user_data['level']}\n"
                           f"🔥 {streak_multiplier:.0f}x multiplier",
                color=0xFEE75C
            )
        else:
            # First hour with fixed width
            embed = discord.Embed(
                description=f"{after.mention} {activity_detected}\n\n"
                           f"`XP:` +{final_xp} • `Total:` {user_data['xp']} • `Level:` {user_data['level']}",
                color=0x57F287
            )
        
        try:
            await log_channel.send(embed=embed)
            logger.info(f"Activity logged: {after.name} - {activity_detected} - {final_xp} XP")
        except Exception as e:
            logger.error(f"Failed to send activity log: {e}")
        
        # Handle level up
        if leveled_up:
            await self.handle_level_up(after, new_level, log_channel)
    
    async def assign_role_for_level(self, member, level, custom_roles, silent=False):
        """Assign appropriate role for a user's level."""
        # Find the highest role the user qualifies for
        qualified_role_level = None
        for role_level in sorted([int(l) for l in custom_roles.keys()], reverse=True):
            if level >= role_level:
                qualified_role_level = role_level
                break
        
        if not qualified_role_level:
            return False
        
        role_id = custom_roles[str(qualified_role_level)]
        role = member.guild.get_role(role_id)
        
        if not role:
            return False
        
        # Check if user already has this role
        if role in member.roles:
            return False
        
        try:
            # Remove all lower level roles
            for level_str, old_role_id in custom_roles.items():
                if int(level_str) != qualified_role_level:
                    old_role = member.guild.get_role(old_role_id)
                    if old_role and old_role in member.roles:
                        await member.remove_roles(old_role)
            
            # Add the appropriate role
            await member.add_roles(role)
            logger.info(f"Assigned {role.name} to {member.name} (Level {level})")
            return True
        except Exception as e:
            logger.error(f"Failed to assign role to {member.name}: {e}")
            return False
    
    async def handle_level_up(self, member, new_level, log_channel):
        """Handle level up and role assignment."""
        guild_id = member.guild.id
        custom_roles = db.get_custom_roles(guild_id)
        
        if not custom_roles:
            return
        
        # Assign appropriate role
        role_assigned = await self.assign_role_for_level(member, new_level, custom_roles)
        
        if role_assigned:
            # Find which role was assigned
            qualified_role_level = None
            for role_level in sorted([int(l) for l in custom_roles.keys()], reverse=True):
                if new_level >= role_level:
                    qualified_role_level = role_level
                    break
            
            if qualified_role_level:
                role_id = custom_roles[str(qualified_role_level)]
                role = member.guild.get_role(role_id)
                
                if role:
                    # Send level up message
                    embed = discord.Embed(
                        title="🎉 LEVEL UP!",
                        description=f"{member.mention} reached **Level {new_level}**!",
                        color=discord.Color.gold()
                    )
                    embed.add_field(name="New Role", value=role.mention, inline=True)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    
                    try:
                        await log_channel.send(embed=embed)
                    except:
                        pass

    @app_commands.command(name="backupxp", description="Backup XP database to JSON (admin only).")
    @app_commands.default_permissions(administrator=True)
    async def backupxp(self, interaction: discord.Interaction):
        """Backup XP database to JSON file."""
        await interaction.response.defer(ephemeral=True)
        
        try:
            filename = db.backup_to_json(f"xp_backup_{interaction.guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            await interaction.followup.send(f"✅ Database backed up to `{filename}`", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Backup failed: {str(e)}", ephemeral=True)
    


async def setup(bot):
    await bot.add_cog(ActivityXP(bot))
