import discord
import asyncio
import random
import datetime
import pytz
import os
from functools import partial
from pymongo import MongoClient
from discord import ButtonStyle, app_commands
from discord.app_commands import Choice
from core.classes import Cog_Extension

def connectdb():
    client = MongoClient('mongodb+srv://')
    return client

async def button1_callback(interaction: discord.Interaction, channels: discord.TextChannel, role_tag: discord.role.Role):
    group_id = interaction.guild.id
    db = Giveaway.client['giveaway']
    table_name = str(group_id)
    giveawaysql = db[table_name]

    user_name = interaction.user.mention
    user_id = interaction.user.id
    channel_id = channels.id
    role_id = role_tag.id

    tz = pytz.timezone('Asia/Taipei')
    datenowtime = datetime.datetime.now(tz)

    time_string = datenowtime.strftime("%Y-%m-%d %H:%M:%S")

    has_permission = False
    for role in interaction.user.roles:
        if role.id == role_id:  
            has_permission = True
            break

    if not has_permission:
        await interaction.response.send_message("很抱歉，您尚未拿取到本次抽獎權限的身分組，請向管理員聯繫或往身分組領取區領取，謝謝 ❗", ephemeral=True)
        return

    # 檢查資料庫中是否存在該使用者
    existing_user = giveawaysql.find_one({'user_id': user_id})

    if existing_user:
        giveawaysql.delete_one({'user_id': user_id})
        await interaction.response.send_message(f"{interaction.user.mention}已幫您退出抽獎名單 ! ", ephemeral=True)
    else:
        data = {'user_name': user_name, 'user_id': user_id, 'channel_id': channel_id, 'time_string': str(time_string)}
        giveawaysql.insert_one(data)
        await interaction.response.send_message(f"{interaction.user.mention}已為您新增到抽獎名單內囉❤️", ephemeral=True)   

async def button2_callback(interaction: discord.Interaction, table: str):
    group_id = interaction.guild.id
    db = Giveaway.client['giveaway']
    table_name = str(group_id)
    giveawaysql = db[table_name]

    user_name = interaction.user.display_name

    user_list = []
    result = giveawaysql.find({})

    for doc in result:
        user_name = doc['user_name']
        time_string = doc['time_string']
        user_info = f"{user_name} - {time_string}"
        user_list.append(user_info)
    if not user_list:
        embed = discord.Embed(title=f"{table} - 本次抽獎名單如下", description="以下是搜尋結果：", color=discord.Color.red())
        embed.add_field(name="查詢無結果", value="找不到符合條件的資料", inline=False)
    else:
        user_info_str = "\n\n".join(user_list)  # 將使用者名稱和 ID 的清單轉為字串
        embed = discord.Embed(title=f"{table} - 本次抽獎名單如下", description=user_info_str, color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

def convert(times):
    pos = ["s", "m", "h", "d", "w"]
    time_dict = {"s": 1, "m": 60, "h": 3600,
                 "d": 3600 * 24, "w": 3600 * 24 * 7}
    unit = times[-1]

    if unit not in pos:
        return -1
    try:
        val = int(times[:-1])
    except:
        return -2

    return val * time_dict[unit]

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

class Giveaway(Cog_Extension):
    client = connectdb()

    @app_commands.command(name="giveaway", description="KOALA BOT 抽獎機系統")
    @app_commands.describe(table="設定抽獎標題", embedcolor="選擇抽獎邊框顏色", channels="設定抽獎頻道", role_tag="設定抽獎通知身分組Tag", times="設定倒數時間[例如:30s] (s(秒)/m(分鐘)/h(小時)/d(天數)/w(週數))", giftname="設定獎品名稱", giveamount="設定獎品數量")
    @app_commands.choices(
        embedcolor = [
            Choice(name="紅色", value="red"),
            Choice(name="藍色", value="blue"),
            Choice(name="綠色", value="green"),
            Choice(name="紫色", value="purple"),
            Choice(name="黃色", value="yellow"),
            Choice(name="金色", value="gold"),
            Choice(name="亮紅色", value="brand_red"),
            Choice(name="暗藍色", value="dark_blue")
        ]
    )
    async def Giveaway(self, interaction: discord.Interaction, embedcolor: Choice[str], channels: discord.TextChannel, role_tag: discord.role.Role, table: str, times: str, giftname: str, giveamount: int):
        group_id = interaction.guild.id

        if embedcolor.value == "red":
            selected_color = discord.Color.red()
        elif embedcolor.value == "blue":
            selected_color = discord.Color.blue()
        elif embedcolor.value == "green":
            selected_color = discord.Color.green()
        elif embedcolor.value == "purple":
            selected_color = discord.Color.purple()
        elif embedcolor.value == "yellow":
            selected_color = discord.Color.yellow()
        elif embedcolor.value == "gold":
            selected_color = discord.Color.gold()
        elif embedcolor.value == "brand_red":
            selected_color = discord.Color.brand_red()
        elif embedcolor.value == "dark_blue":
            selected_color = discord.Color.dark_blue()

        # 自動建立資料表
        db = Giveaway.client['giveaway']
        table_name = str(group_id)  # 使用群組ID作為資料表名稱
        if table_name not in db.list_collection_names():
            db.create_collection(table_name)
        giveawaysql = db[table_name]

        button1 = discord.ui.Button(label="點我加入抽獎名單", style=ButtonStyle.blurple, emoji="🎰")
        button2 = discord.ui.Button(label="查看抽獎名單", style=ButtonStyle.red, emoji="📑")

        button1.callback = partial(button1_callback, channels=channels, role_tag=role_tag)
        button2.callback = partial(button2_callback, table=table)

        view = discord.ui.View(timeout=None)
        view.add_item(button1)
        view.add_item(button2)

        #時間設定問題
        time_seconds = convert(times)
        if time_seconds == -1:
            await interaction.response.send_message("時間格式不正確!", ephemeral=True)
            return
        elif time_seconds == -2:
            await interaction.response.send_message("時間單位必須是整數，例如`3天 = 3d`或`2.5天 = 60h`...等", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{interaction.user.mention} 已經設定並開始進行抽獎囉~ 🎉 在{channels.mention}", ephemeral=True)
        
        tz = pytz.timezone('Asia/Taipei')
        datenowtime = datetime.datetime.now(tz)
        end_time = datenowtime + datetime.timedelta(seconds=time_seconds)
        role_mention = "@everyone" if role_tag.name == "@everyone" else role_tag.mention

        embed = discord.Embed(title="<:KOALA_BOT_em:1108775637616959609> KOALA BOT 抽獎系統", description=f"倒數 {format_time(time_seconds)} 結束", color=selected_color)
        embed.add_field(name="<:giveaway_name:1109440691551088700> 抽獎標題", value=f"```{table}```", inline=False)
        embed.add_field(name="<:giveaway_queue:1109446060708986880> 參與抽獎人數", value=f"```{giveawaysql.count_documents({})}```", inline=True)
        embed.add_field(name="<:koala_group:1108766305760321606> 中獎人數", value=f"```{giveamount}```", inline=True)
        embed.add_field(name="<:koala_gift:1108765792494944338> 獎品", value=f"```{giftname}```", inline=False)
        embed.add_field(name="<:koala_timer:1108766932687147038> 結束時間", value=f"<t:{int(end_time.timestamp())}:f>", inline=False)
        notification_message = await channels.send(content=f"{role_mention}  **抽獎通知來囉~ 🎊**", embed=embed, view=view)

        while time_seconds > 0:
            time_seconds -= 10
            await asyncio.sleep(10)
            new_embed = discord.Embed(title="<:KOALA_BOT_em:1108775637616959609> KOALA BOT 抽獎系統", description=f"倒數 {format_time(time_seconds)} 結束", color=selected_color)
            new_embed.add_field(name="<:giveaway_name:1109440691551088700> 抽獎標題", value=f"```{table}```", inline=False)
            new_embed.add_field(name="<:giveaway_queue:1109446060708986880> 參與抽獎人數", value=f"```{giveawaysql.count_documents({})}```", inline=True)
            new_embed.add_field(name="<:koala_group:1108766305760321606> 中獎人數", value=f"```{giveamount}```", inline=True)
            new_embed.add_field(name="<:koala_gift:1108765792494944338> 獎品", value=f"```{giftname}```", inline=False)
            new_embed.add_field(name="<:koala_timer:1108766932687147038> 結束時間", value=f"<t:{int(end_time.timestamp())}:f>", inline=False)
            await notification_message.edit(content=f"{role_mention}  **抽獎通知來囉~ 🎊**", embed=new_embed)
        
        if time_seconds == 0:
            all_records = list(giveawaysql.find())
            random_record = random.sample(all_records, giveamount)
            winners = [record['user_name'] for record in random_record]  # 中獎者的使用者名稱清單

            embed = discord.Embed(title="<:KOALA_BOT_em:1108775637616959609> KOALA BOT 抽獎系統", description="抽獎倒數結束，已公布中獎者資訊", color=selected_color)
            embed.add_field(name="<:giveaway_name:1109440691551088700> 抽獎標題", value=f"```{table}```", inline=False)
            embed.add_field(name="恭喜中獎者", value="\n".join(winners))  # 在欄位中顯示中獎者的名稱
            await notification_message.edit(content=f"{winners}  **恭喜中獎，獲得【{giftname}】，請開啟客服單或找尋管理人員領取獎品 🎊**", embed=embed, view=None)

            
            with open("giveaway_backup.txt", "w", encoding="utf-8") as file:
                for record in all_records:
                    file.write(str(record) + "\n")
            file = discord.File("giveaway_backup.txt")
            await interaction.user.send(file=file)
            os.remove("giveaway_backup.txt")
    
            await interaction.user.send(f"抽獎已結束，抽獎資料將全數清空")
            giveawaysql.delete_many({})

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
