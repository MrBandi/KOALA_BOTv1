import discord
import asyncio
from datetime import datetime
from discord import ButtonStyle, app_commands
from core.classes import Cog_Extension

class Feedback(discord.ui.Modal):
   def __init__(self, bot):
      super().__init__(title="KOALA BOT 回饋單")
      self.bot = bot
   
   fb_title = discord.ui.TextInput(
      style = discord.TextStyle.short,
      label = "回饋標題",
      required = True,
      placeholder = "請輸入想回饋的標題"
   ) 

   message = discord.ui.TextInput(
      style = discord.TextStyle.long,
      label = "回饋內容",
      required = True,
      max_length = 500,
      placeholder = "請輸入想回饋的內容"
   )

#    myname = discord.ui.TextInput(
#       style = discord.TextStyle.paragraph,
#       label = "回饋測試",
#       required = True,
#       max_length = 500,
#       placeholder = "請輸入想回饋的內容"
#    )

   options = []

   async def on_submit(self, interaction: discord.Interaction):
      self.options.append(self.fb_title.value)
      self.options.append(self.message.value)

      embed = discord.Embed(title="感謝您的回饋，我們會繼續努力 ❗ ", color=discord.Color.blue())
      channel_embed = self.bot.get_channel(1094284463673970849)
      if channel_embed:
          chembed = discord.Embed(title="有人寫回饋單給我們囉~", description="讓我們來看看他們寫的東西吧 ❤", color=discord.Color.orange())
          chembed.add_field(name="**回饋標題**", value=f"```{self.options[0]}```", inline = False)
          chembed.add_field(name="**回饋內容**", value=f"```{self.options[1]}```", inline = False)
          chembed.add_field(name="**填寫者**", value=f"```{interaction.user}```", inline = False)
          timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
          chembed.set_footer(text=f"填寫時間紀錄: {timestamp}")
      await channel_embed.send(embed=chembed)
      await interaction.response.send_message(embed=embed, ephemeral=True)

      
   async def on_error(self, interaction: discord.Interaction, error):
      await interaction.response.send_message("錯誤，請通知bot製作者", ephemeral = True)

class feedbackCog(Cog_Extension):
   @app_commands.command(name="回饋單", description="KOALA BOT回饋單填寫")
   async def feedback(self, interaction: discord.Interaction):
         feedback_modal = Feedback(self.bot)
         await interaction.response.send_modal(feedback_modal)
      
async def setup(bot):
   await bot.add_cog(feedbackCog(bot))
