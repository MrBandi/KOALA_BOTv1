import os
import asyncio
import discord
import time
import subprocess
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "$", intents = intents)

# 當機器人完成啟動時
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    powerlog_channel = bot.get_channel(YOUR LOGS CHANNEL)
    if powerlog_channel:
        embed1 = discord.Embed(title="⚙ KOALA BOT 系統開機紀錄", description=f'本機器人名稱: {bot.user}', color=discord.Color.purple())
        embed1.add_field(name = "本機器人所待在的所有群組如下:(群組名稱+群組ID)", value="--------------------------------", inline=False)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        embed1.set_footer(text=f"紀錄時間: {timestamp}， 群組總數量: {len(bot.guilds)}個")
        for guild in bot.guilds:
            embed1.add_field(name=f"**{guild.name}**", value=f"```{guild.id}```", inline=False)
        await powerlog_channel.send(embed=embed1)

        await bot.change_presence(activity=discord.Game(name="⭐多功能機器人 | PHACS製作"))

    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")

# @bot.command()
# @commands.is_owner()
# async def restart(ctx):
#     restart_message = await ctx.send('Restarting...')
#     subprocess.Popen('python bot.py', shell=True)
#     await bot.close()

#     restarted_message = await restart_message.edit(content='Restart complete.')
#     await asyncio.sleep(5)
#     await restarted_message.delete()

# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    # await ctx.send(f"```已重新Reload {extension} 檔案了```")
    reloadlog = bot.get_channel(1093127348670431262)
    if reloadlog:
        embed = discord.Embed(title="⚙ KOALA BOT 指令重載紀錄",color=discord.Color.red())
        embed.add_field(name = "**重載指令位置**", value = f"```{extension}```", inline=False)
        embed.add_field(name = "**輸入指令者**", value = f"```{ctx.author}```", inline=False)
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        embed.set_footer(text=f"紀錄時間: {timestamp}")
        await reloadlog.send(embed=embed)

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for entry in os.scandir("./cogs"):
        if entry.is_dir():  # 如果是資料夾
            for subentry in os.scandir(entry.path):
                if subentry.is_file() and subentry.name.endswith(".py"):
                    await bot.load_extension(f"cogs.{entry.name}.{subentry.name[:-3]}")
        elif entry.is_file() and entry.name.endswith(".py"):
            await bot.load_extension(f"cogs.{entry.name[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start("YOUR DISCORD BOT TOKEN")

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
