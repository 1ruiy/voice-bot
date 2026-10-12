import discord
from discord.ext import commands
import asyncio
import os

# تفعيل صلاحيات البوت لقراءة حالة الصوت
intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# أيدي الروم الصوتي الخاص بكِ
VOICE_CHANNEL_ID = 1559104968894578749

async def connect_to_voice():
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        # التأكد إذا كان البوت متصلاً بالفعل بالفويس
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

# إعادة الاتصال تلقائياً إذا انقطع أو خرج البوت من الفويس
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        if before.channel is not None and after.channel is None:
            print("⚠️ تم فصل البوت من الفويس، جاري إعادة الاتصال...")
            await asyncio.sleep(5)
            await connect_to_voice()

# جلب توكن البوت من متغيرات البيئة بـ Render لحمايته
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN في متغيرات البيئة (Environment Variables)!")
