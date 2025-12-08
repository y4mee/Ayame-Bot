# cogs/post_commands.py

import discord
from discord import app_commands
from discord.ext import commands
from scraper import fetch_image, fetch_gif
from eporner_fetcher import fetch_eporner_video
from nsfw_data import NSFW_IMAGE_CATEGORIES, NSFW_GIF_CATEGORIES, NSFW_CLIP_CATEGORIES

class PostCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nsfwimg", description="Post a single NSFW image.")
    @app_commands.describe(category="Choose a category")
    async def nsfwimg(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_IMAGE_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        post = await fetch_image(category)
        if post:
            embed = discord.Embed(color=0xED4245)
            embed.set_image(url=post["url"])
            embed.set_footer(text=f"{category.title()} • Image")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)

    @app_commands.command(name="nsfwgif", description="Post a single NSFW gif.")
    @app_commands.describe(category="Choose a category")
    async def nsfwgif(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_GIF_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        post = await fetch_gif(category)
        if post:
            embed = discord.Embed(color=0xF23F42)
            embed.set_image(url=post["url"])
            embed.set_footer(text=f"{category.title()} • GIF")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)

    @app_commands.command(name="nsfwvdo", description="Post a single NSFW video.")
    @app_commands.describe(category="Choose a category")
    async def nsfwvdo(self, interaction: discord.Interaction, category: str):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 NSFW channels only", ephemeral=True)
            return

        if category not in NSFW_CLIP_CATEGORIES:
            await interaction.response.send_message("❌ Invalid category. Use `/list`", ephemeral=True)
            return

        await interaction.response.defer()
        post = await fetch_eporner_video(category)
        if post:
            video_url = post.get("url") or ""
            thumbnail_url = post.get("thumbnail") or "https://cdn.discordapp.com/embed/404.png"
            preview_url = video_url if video_url.endswith(".mp4") else thumbnail_url

            embed = discord.Embed(
                description=f"[**Watch Video**]({post['url']})",
                color=0xEB459E
            )
            embed.set_image(url=preview_url)
            embed.set_footer(text=f"{category.title()} • {post['duration']} min")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("⚠️ Failed to fetch", ephemeral=True)

    @app_commands.command(name="list", description="List all available NSFW categories.")
    async def list_categories(self, interaction: discord.Interaction):
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message("🚫 This command can only be used in NSFW channels.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="Categories",
            color=0x5865F2
        )
        
        # Show all categories cleanly
        image_list = " • ".join(NSFW_IMAGE_CATEGORIES)
        gif_list = " • ".join(NSFW_GIF_CATEGORIES)
        clip_list = " • ".join(NSFW_CLIP_CATEGORIES)
        
        embed.add_field(name="Images", value=image_list, inline=False)
        embed.add_field(name="GIFs", value=gif_list, inline=False)
        embed.add_field(name="Videos", value=clip_list, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PostCommands(bot))
