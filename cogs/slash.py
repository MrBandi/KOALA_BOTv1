import discord
import socket
import pytz
from datetime import datetime
from typing import Optional
from discord import app_commands
from discord.app_commands import Choice
from core.classes import Cog_Extension

class Slash(Cog_Extension):
    # name指令名稱，description指令敘述
    # 主要設定，help幫助。
    # @app_commands.command(name = "help", description = "KOALA BOT 指令使用手冊")
    # async def help(self, interaction: discord.Interaction):
    #     # help幫助
    #     embed = discord.Embed(title="幫助", description="請求幫助！")
    #     embed.add_field(name="指令1", value="這是指令1的說明", inline=False)
    #     embed.add_field(name="指令2", value="這是指令2的說明", inline=False)
    #     await interaction.response.send_message(embed=embed)

    # 功能一，主機端口查詢
    @app_commands.command(name = "portcheck", description = "主機端口檢測")
    @app_commands.describe(ip = "輸入主機IP", port = "輸入主機端口")
    async def portcheck(self, interaction: discord.Interaction, ip: str, port: str):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            result = s.connect_ex((ip, int(port)))
            if result == 0:
                embed = discord.Embed(title="KOALA BOT 主機端口檢測結果", description="Test")
                embed.add_field(name="**主機IP及端口**", value=f"```{ip} : {port}```", inline=False)
                embed.add_field(name="**主機端口狀態**", value="`🟢`\n此主機IP該端口為開啟狀態", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="KOALA BOT 主機端口檢測結果")
                embed.add_field(name="**主機IP及端口**", value=f"```{ip} : {port}```", inline=False)
                embed.add_field(name="**主機端口狀態**", value="`🔴`\n此主機IP該端口為未開啟狀態", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            s.close()
        except:
            embed = discord.Embed(title="KOALA BOT 主機端口檢測結果")
            embed.add_field(name="**主機IP及端口**", value=f"```{ip}:{port}```", inline=False)
            embed.add_field(name="**主機端口狀態**", value="`🔴`\n此主機IP該端口為未開啟狀態", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # 參數: Optional[資料型態]，參數變成可選，可以限制使用者輸入的內容
    @app_commands.command(name = "dns", description = "網域DNS查詢")
    @app_commands.describe(domain = "輸入網域")
    async def dns(self, interaction: discord.Interaction, domain: str):
        try:
        # Perform DNS lookup
            results = socket.getaddrinfo(domain, None)
        
        # Parse results and extract IP addresses
            ips = [result[4][0] for result in results]
        
        # Send response
            if ips:
                await interaction.response.send_message(f"**『DNS查詢』此網域已偵測到紀錄。**\n**此網域IPv4登記紀錄: {', '.join(ips)}**")
            else:
                await interaction.response.send_message("『DNS查詢』 查詢不成功，有可能您的網域不是有效的網域。")    
        except socket.gaierror as e:
            await interaction.response.send_message(f"『DNS查詢』查詢失敗: {e}")

    #SteamID轉換16進制
    @app_commands.command(name="steam16", description="將SteamID轉換成16進制")
    @app_commands.describe(steamid="輸入用戶ID")
    async def steam16(self, interaction: discord.Interaction, steamid: str):
        steamid = steamid.strip()
        if steamid.isdigit():
            steamid = int(steamid)
            hexid = hex(steamid)[2:]
            embed = discord.Embed(title="**SteamID轉換16進制**", description="歡迎使用此功能!")
            embed.add_field(name="**轉換前的SteamID**", value=f"{steamid}", inline=False)
            embed.add_field(name="**轉換後的16進制ID**", value=f"{hexid}", inline=False)
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            embed.set_footer(text=f"轉換時間: {timestamp}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("請輸入有效的 SteamID。", ephemeral=True)

    # @app_commands.choices(參數 = [Choice(name = 顯示名稱, value = 隨意)])
    @app_commands.command(name = "order", description = "點餐機")
    @app_commands.describe(meal = "選擇餐點", size = "選擇份量")
    @app_commands.choices(
        meal = [
            Choice(name = "漢堡", value = "hamburger"),
            Choice(name = "薯條", value = "fries"),
            Choice(name = "雞塊", value = "chicken_nuggets"),
        ],
        size = [
            Choice(name = "大", value = 0),
            Choice(name = "中", value = 1),
            Choice(name = "小", value = 2),
        ]
    )
    async def order(self, interaction: discord.Interaction, meal: Choice[str], size: Choice[int]):
        # 獲取使用指令的使用者名稱
        customer = interaction.user.name
        # 使用者選擇的選項資料，可以使用name或value取值
        meal = meal.value
        size = size.value
        await interaction.response.send_message(f"{customer} 點了 {size} 號 {meal} 餐")

async def setup(bot):
    await bot.add_cog(Slash(bot))
