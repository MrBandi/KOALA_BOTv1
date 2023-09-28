import discord
from discord import app_commands
from core.classes import Cog_Extension

class Invite(Cog_Extension):
    @app_commands.command(name="invite", description = "邀請機器人連結")
    async def invite(self, interaction: discord.Interaction):
        embed = discord.Embed(title="點我下方的按鈕來邀請我進入你的伺服器服務吧~🫠", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, view=InviteButton())

class InviteButton(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="🫱🏽‍🫲🏽邀請我", url="https://discord.com/api/oauth2/authorize?client_id="))

async def setup(bot):
    await bot.add_cog(Invite(bot))