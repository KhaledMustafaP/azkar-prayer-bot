import logging
import asyncio
import requests
import nest_asyncio
import schedule
import pytz
from datetime import datetime
from telegram import Bot
from telegram.ext import Application, CommandHandler
from flask import Flask
import threading

# === إعدادات البوت ===
BOT_TOKEN = "8075622956:AAEKedhb3JAIOWlSx_vn3kGZOoPhiYwscJo"
CHAT_ID = "@wahmidf"

# إعداد الموقع
CITY = "Amman"
COUNTRY = "Jordan"
TIMEZONE = "Asia/Amman"

# تهيئة
logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()
app = Application.builder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
local_tz = pytz.timezone(TIMEZONE)

# ملف العداد
def read_juz():
    try:
        with open("progress.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 1

def write_juz(juz):
    with open("progress.txt", "w") as file:
        file.write(str(juz))

# ورد يومي
async def send_daily_ward():
    juz = read_juz()
    msg = f"📖 وردك اليومي: الجزء ({juz}) - لا تنسَ تلاوة ما تيسر من القرآن 💚"
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)
    next_juz = 1 if juz == 30 else juz + 1
    write_juz(next_juz)

# أذكار
async def send_morning_azkar():
    msg = "☀️ أذكار الصباح:\n- اللهم بك أصبحنا...\n- بسم الله الذي لا يضر...\n- أصبحنا وأصبح الملك لله...\n🕊️ واذكر الله كثيرًا."
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

async def send_evening_azkar():
    msg = "🌙 أذكار المساء:\n- اللهم بك أمسينا...\n- بسم الله الذي لا يضر...\n- أمسينا وأمسى الملك لله...\n🕊️ واذكر الله قبل النوم."
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

# مواقيت الصلاة
def get_today_prayer_times():
    url = f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=2"
    response = requests.get(url)
    data = response.json()

    if data['code'] != 200:
        return None

    return {
        "Fajr": data['data']['timings']['Fajr'],
        "Dhuhr": data['data']['timings']['Dhuhr'],
        "Asr": data['data']['timings']['Asr'],
        "Maghrib": data['data']['timings']['Maghrib'],
        "Isha": data['data']['timings']['Isha']
    }

async def send_prayer_times():
    times = get_today_prayer_times()
    if not times:
        await app.bot.send_message(chat_id=CHAT_ID, text="❌ فشل في جلب مواقيت الصلاة.")
        return

    message = "🕌 مواقيت الصلاة اليوم في عمّان:\n"
    message += f"📿 الفجر: {times['Fajr']}\n"
    message += f"🌅 الشروق: {data['data']['timings']['Sunrise']}\n"
    message += f"🏙️ الظهر: {times['Dhuhr']}\n"
    message += f"🌇 العصر: {times['Asr']}\n"
    message += f"🌆 المغرب: {times['Maghrib']}\n"
    message += f"🌌 العشاء: {times['Isha']}"
    await app.bot.send_message(chat_id=CHAT_ID, text=message)

# سنن الصلوات
prayer_sunnah = {
    "Fajr": "🌄 سنة الفجر: ركعتان قبلية مؤكدة",
    "Dhuhr": "🌞 سنة الظهر: 4 قبلية + 2 بعدية",
    "Asr": "🌤️ سنة العصر: 4 قبلية غير مؤكدة",
    "Maghrib": "🌇 سنة المغرب: 2 بعدية",
    "Isha": "🌙 سنة العشاء: 2 بعدية + الوتر"
}

# تذكير عند الصلاة
async def send_prayer_reminder(prayer_name):
    msg = f"🕌 حان الآن وقت صلاة {prayer_name}.\n{prayer_sunnah.get(prayer_name, '')}"
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

def create_reminder_task(prayer):
    return lambda: asyncio.create_task(send_prayer_reminder(prayer))

def schedule_prayer_reminders():
    schedule.clear('prayers')
    times = get_today_prayer_times()
    if not times:
        return
    for prayer, time_str in times.items():
        schedule.every().day.at(time_str).do(create_reminder_task(prayer)).tag('prayers')

# الأوامر
async def start(update, context):
    await update.message.reply_text("🌞 بوت ورد كالشمس! يرسل ورد يومي، أذكار، وتذكير بالصلاة.")

async def now_command(update, context):
    await send_prayer_times()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("now", now_command))

# المهام المجدولة
def schedule_tasks():
    schedule.every().day.at("06:00").do(lambda: asyncio.create_task(send_daily_ward()))
    schedule.every().day.at("06:01").do(lambda: asyncio.create_task(send_prayer_times()))
    schedule.every().day.at("10:00").do(lambda: asyncio.create_task(send_morning_azkar()))
    schedule.every().day.at("17:00").do(lambda: asyncio.create_task(send_evening_azkar()))

    schedule_prayer_reminders()
    schedule.every().day.at("00:01").do(schedule_prayer_reminders)

# السيرفر للفحص
@flask_app.route('/')
def home():
    return "✅ البوت يعمل"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000)

# تشغيل البوت
async def main():
    await app.bot.send_message(chat_id=CHAT_ID, text="✅ تم تشغيل البوت.")
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    threading.Thread(target=run_web).start()
    await app.run_polling()

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
