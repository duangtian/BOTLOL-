import discord
from discord.ext import tasks
import asyncio
from datetime import datetime
import pytz
import os

# ===== ตั้งค่าตรงนี้ =====
BOT_TOKEN = os.environ["BOT_TOKEN"]     # ดึงจาก environment variable
CHANNEL_ID = int(os.environ["CHANNEL_ID"])  # ใส่ใน Railway Variables
ROLE_NAME = "L++"                        # ชื่อ role ที่จะ tag
TIMEZONE = "Asia/Bangkok"                # timezone ไทย
# =========================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot พร้อมแล้ว: {client.user}")
    daily_notify.start()

@tasks.loop(minutes=1)
async def daily_notify():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    # ส่งตอน 21:00 (สามทุ่มตรง)
    if now.hour == 21 and now.minute == 0:
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            print("❌ ไม่เจอ channel")
            return

        # หา role @L++
        guild = channel.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        if role:
            await channel.send(f"{role.mention} 🔔 สามทุ่มแล้ว!")
        else:
            await channel.send(f"@{ROLE_NAME} 🔔 สามทุ่มแล้ว! (ไม่เจอ role)")

        print(f"✅ ส่ง noti แล้วตอน {now.strftime('%H:%M')}")

client.run(BOT_TOKEN)
