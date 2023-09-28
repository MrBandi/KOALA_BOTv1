import discord
import requests
import datetime
from discord import app_commands
from core.classes import Cog_Extension

class Mcid(Cog_Extension):
    @app_commands.command(name="mcid", description = "查詢Minecraft玩家資料")
    @app_commands.describe(id = "輸入玩家ID")
    async def get_minecraft_data(self, interaction: discord.Interaction, id: str):
        url = f"https://api.mojang.com/users/profiles/minecraft/{id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            uuid = data["id"]
            name = data["name"]
            url = f"https://crafatar.com/avatars/{uuid}"
            embed = discord.Embed(title=name, color=0x00ff00)
            embed.set_image(url=url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("找不到該玩家的 Minecraft 資料")

async def setup(bot):
    await bot.add_cog(Mcid(bot))