import discord
import datetime
import time
import asyncio
from discord import app_commands
from core.classes import Cog_Extension


class Ping(Cog_Extension):
   @app_commands.command(name="ping", description="查看機器人延遲")
   async def ping(self, interaction: discord.Interaction):
      latency = round(self.bot.latency * 1000)
      start_time = time.time()
      await asyncio.sleep(0.1)
      measured_time = time.time() - start_time
      end = round(measured_time * 1000)
      if latency < 250:
         color = discord.Color.blue()
      elif latency < 450:
         color = discord.Color.green()
      elif latency < 600:
         color = discord.Color.orange()
      elif latency < 800:
         color = discord.Color.red()
      else:
         color = discord.Color.dark_red()

      embed = discord.Embed(title=f":ping_pong: Pong!", color=color, timestamp=datetime.datetime.utcnow())
      embed.add_field(name="網路連接", value=f"```{latency} ms```", inline=False)
      embed.add_field(name="延遲", value=f"```{end} ms```", inline=False)
      await interaction.response.send_message(embed=embed)

async def setup(bot):
   await bot.add_cog(Ping(bot))
