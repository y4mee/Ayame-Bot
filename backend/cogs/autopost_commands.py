# cogs/autopost_commands.py

import discord
from discord import app_commands
from discord.ext import commands
from scraper import fetch_image, fetch_gif
from eporner_fetcher import fetch_eporner_video
from nsfw_data import NSFW_IMAGE_CATEGORIES, NSFW_GIF_CATEGORIES, NSFW_CLIP_CATEGORIES
import logging

logger = logging.getLogger(__name__)

class AutoPostButton(discord.ui.View):
    def __init__(self, media_type: str, category: str, user_id: int, fetch_func):
        super().__init__(timeout=None)  # No timeout - works indefinitely
        self.media_type = media_type
        self.category = category
        self.user_id = user_id
        self.fetch_func = fetch_func

    @discord.ui.button(label="⟳", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Anyone can click the button
        await interaction.response.defer(thinking=False)

        post = await self.fetch_func(self.category)
        if not post:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)
            return

        # Clean, minimal embed
        if self.media_type == "clip":
            preview_url = (
                post["url"] if post["url"].endswith(".mp4")
                else post.get("thumbnail") or "https://cdn.discordapp.com/embed/404.png"
            )
            embed = discord.Embed(
                description=f"[**Watch Video**]({post.get('url')})",
                color=0xEB459E
            )
            embed.set_image(url=preview_url)
            embed.set_footer(text=f"{self.category.title()} • {post.get('duration', 'N/A')} min")
        else:
            # Image or GIF
            color = 0xED4245 if self.media_type == "image" else 0xF23F42
            embed = discord.Embed(color=color)
            embed.set_image(url=post["url"])
            embed.set_footer(text=f"{self.category.title()} • {self.media_type.upper()}")

        # Create NEW view with buttons for THIS post
        new_view = AutoPostButton(self.media_type, self.category, self.user_id, self.fetch_func)
        
        # Send new content WITH buttons
        await interaction.followup.send(embed=embed, view=new_view)
        logger.info(f"{interaction.user} fetched next {self.media_type} from {self.category}")

    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Only the person who started can stop
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Only starter can stop", ephemeral=True)
            return
        
        await interaction.response.send_message("✅ Stopped", ephemeral=True)
        await interaction.message.delete()
        logger.info(f"{interaction.user} stopped autopost in {interaction.channel}")


class AutoPost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="autonsfwimg", description="Auto-post NSFW images with button.")
    @app_commands.describe(category="Category to post from")
    async def autonsfwimg(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_IMAGE_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        
        # Fetch first post immediately
        post = await fetch_image(category)
        if not post:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)
            return
        
        # Create embed with first post
        embed = discord.Embed(color=0xED4245)
        embed.set_image(url=post["url"])
        embed.set_footer(text=f"{category.title()} • Image")
        
        # Add buttons to this post
        view = AutoPostButton("image", category, interaction.user.id, fetch_image)
        
        await interaction.followup.send(embed=embed, view=view)
        logger.info(f"{interaction.user} started autopost: image - {category}")

    @app_commands.command(name="autonsfwgif", description="Auto-post NSFW gifs with button.")
    @app_commands.describe(category="Category to post from")
    async def autonsfwgif(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_GIF_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        
        # Fetch first post immediately
        post = await fetch_gif(category)
        if not post:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)
            return
        
        # Create embed with first post
        embed = discord.Embed(color=0xF23F42)
        embed.set_image(url=post["url"])
        embed.set_footer(text=f"{category.title()} • GIF")
        
        # Add buttons to this post
        view = AutoPostButton("gif", category, interaction.user.id, fetch_gif)
        
        await interaction.followup.send(embed=embed, view=view)
        logger.info(f"{interaction.user} started autopost: gif - {category}")

    @app_commands.command(name="autonsfwvdo", description="Auto-post NSFW videos with button.")
    @app_commands.describe(category="Category to post from")
    async def autonsfwvdo(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_CLIP_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        
        # Fetch first post immediately
        post = await fetch_eporner_video(category)
        if not post:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)
            return
        
        # Create embed with first post
        video_url = post.get("url") or ""
        thumbnail_url = post.get("thumbnail") or "https://cdn.discordapp.com/embed/404.png"
        preview_url = video_url if video_url.endswith(".mp4") else thumbnail_url

        embed = discord.Embed(
            description=f"[**Watch Video**]({post['url']})",
            color=0xEB459E
        )
        embed.set_image(url=preview_url)
        embed.set_footer(text=f"{category.title()} • {post['duration']} min")
        
        # Add buttons to this post
        view = AutoPostButton("clip", category, interaction.user.id, fetch_eporner_video)
        
        await interaction.followup.send(embed=embed, view=view)
        logger.info(f"{interaction.user} started autopost: clip - {category}")




async def setup(bot):
    await bot.add_cog(AutoPost(bot))
