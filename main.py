import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

# سيرفر وهمي يبقي البوت شغّالاً على الخطة المجانية
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال 24/7 بنجاح!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# إعدادات البوت
intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

VOICE_CHANNEL_ID = 1559104968894578749

async def connect_to_voice():
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        for vc in bot.voice_clients:
            if vc.channel.id == channel.id:
                return
            await vc.disconnect()
        
        try:
            await channel.connect(reconnect=True, timeout=30.0)
            print(f"✅ تم الدخول بنجاح إلى الروم الصوتي: {channel.name}")
        except Exception as e:
            print(f"❌ حدث خطأ أثناء محاولة الاتصال بالروم: {e}")

@bot.event
async def on_ready():
    print(f"🤖 البوت شغال باسم: {bot.user}")
    await connect_to_voice()

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        if before.channel is not None and after.channel is None:
            print("⚠️ تم فصل البوت من الفويس، جاري إعادة الاتصال...")
            await asyncio.sleep(5)
            await connect_to_voice()

# تشغيل السيرفر والبوت
keep_alive()

token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN في متغيرات البيئة!")

