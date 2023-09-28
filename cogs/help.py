import discord
from discord import app_commands
from core.classes import Cog_Extension

class HelpList(discord.ui.Select):
   def __init__(self):
        options = [
            discord.SelectOption(label="一般功能", emoji="🧬", description="一堆你會用到的功能"),
            discord.SelectOption(label="群組功能", emoji="👨‍👨‍👧‍👧", description="協助管理群組的功能"),
            discord.SelectOption(label="樂趣功能", emoji="🎮", description="可以玩的小遊戲功能")
        ]

        super().__init__(options=options)

class Help(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="help", description="KOALA BOT TEST 功能查詢")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"<:KOALA_BOT_em:1108775637616959609> {self.bot.user.name} 功能列表介紹", description="歡迎使用KOALA 多功能機器人 | 幻空雲海PHACS 團隊所製作✨\n點選下方的選單可以來查看我們有那些功能，希望你會喜歡❤\n</help:1109823170363531366>")

        view = discord.ui.View()
        view.add_item(HelpList())

        await interaction.response.send_message(embed=embed, view=view)
        

async def setup(bot):
   await bot.add_cog(Help(bot))
