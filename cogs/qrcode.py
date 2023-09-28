import discord
import qrcode
from discord import app_commands
from core.classes import Cog_Extension

class Qrcode(Cog_Extension):
    @app_commands.command(name="qrcode", description="把URL網址轉換成QRcode碼，方便使用")
    @app_commands.describe(url = "貼上想要轉成QRcode的Url網址")
    async def comd(self, interaction: discord.Interaction, url: str):
        qr = qrcode.QRCode(version=None, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qrcode.png")
        await interaction.response.send_message(file=discord.File("qrcode.png"), ephemeral=True)
        
async def setup(bot):
   await bot.add_cog(Qrcode(bot))
