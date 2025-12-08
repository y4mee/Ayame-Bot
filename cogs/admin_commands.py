import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Check if user has administrator permissions."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You need Administrator permissions to use this command.",
                ephemeral=True
            )
            return False
        return True

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for the ban",
        delete_messages="Delete messages from last X days (0-7)"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
        delete_messages: int = 0
    ):
        await interaction.response.defer(ephemeral=True)
        
        if member.top_role >= interaction.user.top_role:
            await interaction.followup.send("❌ You cannot ban someone with equal or higher role.", ephemeral=True)
            return
        
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot ban yourself.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason, delete_message_days=min(delete_messages, 7))
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"**{member.mention}** has been banned.",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            await interaction.followup.send(embed=embed)
            logger.info(f"{interaction.user} banned {member} for: {reason}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to ban: {str(e)}", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user from the server.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(user_id="The user ID to unban", reason="Reason for unbanning")
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        await interaction.response.defer(ephemeral=True)
        
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=reason)
            embed = discord.Embed(
                title="✅ User Unbanned",
                description=f"**{user.mention}** has been unbanned.",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            await interaction.followup.send(embed=embed)
            logger.info(f"{interaction.user} unbanned {user} for: {reason}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to unban: {str(e)}", ephemeral=True)

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="The member to kick", reason="Reason for the kick")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await interaction.response.defer(ephemeral=True)
        
        if member.top_role >= interaction.user.top_role:
            await interaction.followup.send("❌ You cannot kick someone with equal or higher role.", ephemeral=True)
            return
        
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot kick yourself.", ephemeral=True)
            return

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.mention}** has been kicked.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            await interaction.followup.send(embed=embed)
            logger.info(f"{interaction.user} kicked {member} for: {reason}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to kick: {str(e)}", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="The member to timeout",
        duration="Duration in minutes",
        reason="Reason for timeout"
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: int,
        reason: str = "No reason provided"
    ):
        await interaction.response.defer(ephemeral=True)
        
        if member.top_role >= interaction.user.top_role:
            await interaction.followup.send("❌ You cannot timeout someone with equal or higher role.", ephemeral=True)
            return
        
        if member.id == interaction.user.id:
            await interaction.followup.send("❌ You cannot timeout yourself.", ephemeral=True)
            return

        try:
            timeout_duration = timedelta(minutes=duration)
            await member.timeout(timeout_duration, reason=reason)
            embed = discord.Embed(
                title="⏰ Member Timed Out",
                description=f"**{member.mention}** has been timed out for **{duration} minutes**.",
                color=discord.Color.yellow()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            await interaction.followup.send(embed=embed)
            logger.info(f"{interaction.user} timed out {member} for {duration}m: {reason}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to timeout: {str(e)}", ephemeral=True)

    @app_commands.command(name="untimeout", description="Remove timeout from a member.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="The member to remove timeout from")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)
        
        try:
            await member.timeout(None)
            embed = discord.Embed(
                title="✅ Timeout Removed",
                description=f"**{member.mention}** timeout has been removed.",
                color=discord.Color.green()
            )
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            await interaction.followup.send(embed=embed)
            logger.info(f"{interaction.user} removed timeout from {member}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to remove timeout: {str(e)}", ephemeral=True)

    @app_commands.command(name="purge", description="Delete multiple messages.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        
        if amount < 1 or amount > 100:
            await interaction.followup.send("❌ Amount must be between 1 and 100.", ephemeral=True)
            return

        try:
            deleted = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"✅ Deleted **{len(deleted)}** messages.", ephemeral=True)
            logger.info(f"{interaction.user} purged {len(deleted)} messages in {interaction.channel}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to purge: {str(e)}", ephemeral=True)

    @app_commands.command(name="clear", description="Clear messages from a specific user.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="The member whose messages to clear", amount="Number of messages to check (1-100)")
    async def clear(self, interaction: discord.Interaction, member: discord.Member, amount: int = 50):
        await interaction.response.defer(ephemeral=True)
        
        if amount < 1 or amount > 100:
            await interaction.followup.send("❌ Amount must be between 1 and 100.", ephemeral=True)
            return

        try:
            deleted = await interaction.channel.purge(limit=amount, check=lambda m: m.author == member)
            await interaction.followup.send(
                f"✅ Deleted **{len(deleted)}** messages from {member.mention}.",
                ephemeral=True
            )
            logger.info(f"{interaction.user} cleared {len(deleted)} messages from {member}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to clear: {str(e)}", ephemeral=True)

    @app_commands.command(name="slowmode", description="Set slowmode for the channel.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(seconds="Slowmode delay in seconds (0 to disable, max 21600)")
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        await interaction.response.defer(ephemeral=True)
        
        if seconds < 0 or seconds > 21600:
            await interaction.followup.send("❌ Seconds must be between 0 and 21600 (6 hours).", ephemeral=True)
            return

        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.followup.send("✅ Slowmode disabled.", ephemeral=True)
            else:
                await interaction.followup.send(f"✅ Slowmode set to **{seconds}** seconds.", ephemeral=True)
            logger.info(f"{interaction.user} set slowmode to {seconds}s in {interaction.channel}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to set slowmode: {str(e)}", ephemeral=True)

    @app_commands.command(name="lock", description="Lock the channel (prevent members from sending messages).")
    @app_commands.default_permissions(administrator=True)
    async def lock(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.followup.send("🔒 Channel locked.", ephemeral=True)
            logger.info(f"{interaction.user} locked {interaction.channel}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to lock: {str(e)}", ephemeral=True)

    @app_commands.command(name="unlock", description="Unlock the channel.")
    @app_commands.default_permissions(administrator=True)
    async def unlock(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        try:
            overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = None
            await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            await interaction.followup.send("🔓 Channel unlocked.", ephemeral=True)
            logger.info(f"{interaction.user} unlocked {interaction.channel}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to unlock: {str(e)}", ephemeral=True)

    @app_commands.command(name="nick", description="Change a member's nickname.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="The member to rename", nickname="New nickname (leave empty to reset)")
    async def nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str = None):
        await interaction.response.defer(ephemeral=True)
        
        if member.top_role >= interaction.user.top_role and member.id != interaction.user.id:
            await interaction.followup.send("❌ You cannot change nickname of someone with equal or higher role.", ephemeral=True)
            return

        try:
            old_nick = member.display_name
            await member.edit(nick=nickname)
            new_nick = nickname if nickname else member.name
            embed = discord.Embed(
                title="✏️ Nickname Changed",
                description=f"**{member.mention}** nickname updated.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Old Nickname", value=old_nick, inline=True)
            embed.add_field(name="New Nickname", value=new_nick, inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user} changed {member}'s nickname to {new_nick}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to change nickname: {str(e)}", ephemeral=True)

    @app_commands.command(name="role", description="Add or remove a role from a member.")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(
        member="The member to modify",
        role="The role to add/remove",
        action="Add or remove the role"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add", value="add"),
        app_commands.Choice(name="Remove", value="remove")
    ])
    async def role(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role,
        action: str
    ):
        await interaction.response.defer(ephemeral=True)
        
        if role >= interaction.user.top_role:
            await interaction.followup.send("❌ You cannot manage a role equal or higher than yours.", ephemeral=True)
            return

        try:
            if action == "add":
                if role in member.roles:
                    await interaction.followup.send(f"❌ {member.mention} already has {role.mention}.", ephemeral=True)
                    return
                await member.add_roles(role)
                await interaction.followup.send(f"✅ Added {role.mention} to {member.mention}.", ephemeral=True)
                logger.info(f"{interaction.user} added {role} to {member}")
            else:
                if role not in member.roles:
                    await interaction.followup.send(f"❌ {member.mention} doesn't have {role.mention}.", ephemeral=True)
                    return
                await member.remove_roles(role)
                await interaction.followup.send(f"✅ Removed {role.mention} from {member.mention}.", ephemeral=True)
                logger.info(f"{interaction.user} removed {role} from {member}")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to modify role: {str(e)}", ephemeral=True)

    @app_commands.command(name="warn", description="Warn a member (sends them a DM).")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(member="The member to warn", reason="Reason for the warning")
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await interaction.response.defer(ephemeral=True)
        
        try:
            embed = discord.Embed(
                title="⚠️ Warning",
                description=f"You have been warned in **{interaction.guild.name}**.",
                color=discord.Color.yellow()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.name, inline=True)
            embed.set_footer(text="Please follow the server rules.")
            
            await member.send(embed=embed)
            await interaction.followup.send(f"✅ Warned {member.mention} for: {reason}", ephemeral=True)
            logger.info(f"{interaction.user} warned {member} for: {reason}")
        except discord.Forbidden:
            await interaction.followup.send(f"⚠️ Could not DM {member.mention}, but warning logged.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to warn: {str(e)}", ephemeral=True)

    @app_commands.command(name="serverinfo", description="Display server information.")
    @app_commands.default_permissions(administrator=True)
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        embed.set_footer(text=f"Server ID: {guild.id}")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
