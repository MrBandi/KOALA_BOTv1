import discord
from discord import app_commands
from core.classes import Cog_Extension

class Comd(Cog_Extension):
    @app_commands.command(name="comd", description="不會算IP的，來使用者個指令，我來教你")
    @app_commands.describe(popr = "輸入IP位置斜線後面的數字", server = "輸入伺服器給的IP，最後一個點之後的數字")
    async def comd(self, interaction: discord.Interaction, popr: int, server: int):
        a = 27
        b = 26
        c = 25
        d = 24
        net = 256

        if popr == a or b or c or d:
            j = popr - d
            if j == 3:
                f = 2**7 + 2**6 + 2**5
            elif j == 2:
                f = 2**7 + 2**6
            elif j == 1:
                f = 2**7
            elif j == 0:
                f = 0
            start = net-f
            w = round(server/start,1)
            k = w // 1
            out = k*start
            embed = discord.Embed(title="**網路架設丙級術科-IP計算**", description="IP計算，最快速的方法")
            embed.add_field(name="輸入斜線後面的數字", value=f"{popr}", inline= True)
            embed.add_field(name="伺服器IP位置最後的數字", value=f"{server}", inline= True)
            embed.add_field(name="計算結果 - 預設遮罩", value=f"{f}", inline= False)
            embed.add_field(name="計算結果 - 伺服器起始位置", value=f"{int(out)}", inline= False)
            embed.add_field(name="下方計算過程", value=f"{popr} - {d} = {j}\n出現3 = 128+64+32，出現2 = 128+64\n出現1 = 128，出現0 = 0\n預設遮罩 = {f}\n{net} - {f} = {start}\n再用 {server} 去除 {start}\n最後 = {int(out)} 就是伺服器起始位置", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
   await bot.add_cog(Comd(bot))
