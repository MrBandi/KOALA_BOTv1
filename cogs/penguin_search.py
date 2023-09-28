import discord
import datetime
from functools import partial
from pymongo import MongoClient
from discord import ButtonStyle, app_commands
from core.classes import Cog_Extension

def connectdb():
   client = MongoClient('mongodb+srv://')
   db = client['penguin_group']
   return db

buttontext = ['minecraft_bedwars', 'valorant', 'fallguys', 'crabgame', 'csgo']

async def button_callback(interaction: discord.Interaction, text):
   db = Penguin_Search.db[text]

   player_list = []
   result = db.find({})

   for doc in result:
      user_name = doc['player_name']
      time_string = doc['apply_time']
      userinfo = f"{user_name}  -  {time_string}"
      player_list.append(userinfo)

   if not player_list:
      embed = discord.Embed(title="活動報名查詢", description="查詢資料如下:", color=discord.Color.red())
      embed.add_field(name="查詢無結果", value="目前無人報名", inline=False)
   else:
      user_info_str = "\n\n".join(player_list)
      embed = discord.Embed(title="活動報名查詢", description="查詢資料如下:", color=discord.Color.gold())
      embed.add_field(name="查詢項目", value=f"`{text}`", inline=False)
      embed.add_field(name="報名資訊", value=f"```{user_info_str}```", inline=True)

   await interaction.response.send_message(embed=embed, ephemeral=True)

class Penguin_Search(Cog_Extension):
   db = connectdb()

   @app_commands.command(name="penguin-search", description="🐧企鵝窩DISCORD群組-查詢")
   async def penguinsearch(self, interaction: discord.Interaction):
      group_id = interaction.guild.id
      user_id = interaction.user.id
      owner_id = [685803144684634132, 718418472283013201]

      button_mc = discord.ui.Button(label="Bedwars", style=ButtonStyle.blurple, row=1)
      button_val = discord.ui.Button(label="Valorant", style=ButtonStyle.blurple, row=1)
      button_cs = discord.ui.Button(label="Csgo", style=ButtonStyle.blurple, row=1)
      button_fall = discord.ui.Button(label="Fallguys", style=ButtonStyle.blurple, row=2)
      button_crabgame = discord.ui.Button(label="Crabgame", style=ButtonStyle.blurple, row=2)


      if group_id == 685839828314882078 and user_id in owner_id:
         button_mc.callback = partial(button_callback, text=buttontext[0])
         button_val.callback = partial(button_callback, text=buttontext[1])
         button_cs.callback = partial(button_callback, text=buttontext[4])
         button_fall.callback = partial(button_callback, text=buttontext[2])
         button_crabgame.callback = partial(button_callback, text=buttontext[3])
         embed = discord.Embed(title="活動報名查詢", description="此指令限定企鵝窩群組")

         view = discord.ui.View(timeout=None)
         view.add_item(button_mc)
         view.add_item(button_val)
         view.add_item(button_cs)
         view.add_item(button_fall)
         view.add_item(button_crabgame)
         await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
      else:
         await interaction.response.send_message(content="這裡不是企鵝窩的群組", ephemeral=True)


async def setup(bot):
   await bot.add_cog(Penguin_Search(bot))