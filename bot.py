import logging
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler
import nest_asyncio
import schedule
from datetime import datetime, date
import pytz
import threading
from flask import Flask
from praytimes import PrayTimes

# === إعدادات البوت ===
BOT_TOKEN = "YOUR_TOKEN_HERE"
CHAT_ID = "@your_channel_or_id"

# === إعداد الموقع === (عمان، الأردن كمثال)
latitude = 31.9539
longitude = 35.9106
timezone = 3  # UTC+3 for Jordan

# === تهيئة ===
logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()
app = Application.builder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
pt = PrayTimes("MWL")

# === ورد يومي ===
def read_juz():
    try:
        with open("progress.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 1

def write_juz(juz):
    with open("progress.txt", "w") as file:
        file.write(str(juz))

async def send_daily_ward():
    juz = read_juz()
    msg = f"📖 وردك اليومي: الجزء ({juz}) - لا تنسَ تلاوة ما تيسر من القرآن اليوم 💚"
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)
    next_juz = 1 if juz == 30 else juz + 1
    write_juz(next_juz)

# === أذكار ===
async def send_morning_azkar():
    msg = "☀️ أذكار الصباح:\n- اللهم بك أصبحنا...\n- بسم الله الذي لا يضر...\n- أصبحنا وأصبح الملك لله...\n🕊️ واذكر الله كثيرًا."
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

async def send_evening_azkar():
    msg = "🌙 أذكار المساء:\n- اللهم بك أمسينا...\n- بسم الله الذي لا يضر...\n- أمسينا وأمسى الملك لله...\n🕊️ واذكر الله قبل النوم."
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

# === سنن الصلوات ===
prayer_sunnah = {
    "Fajr": "🌄 سنة الفجر: ركعتان قبلية مؤكدة",
    "Dhuhr": "🌞 سنة الظهر: 4 قبلية + 2 بعدية",
    "Asr": "🌤️ سنة العصر: 4 قبلية غير مؤكدة",
    "Maghrib": "🌇 سنة المغرب: 2 بعدية",
    "Isha": "🌙 سنة العشاء: 2 بعدية + الوتر"
}

# === أوقات الصلاة وتذكير ===
def get_today_prayer_times():
    today = date.today()
    times = pt.getTimes(today, (latitude, longitude), timezone)
    return {
        "Fajr": times["fajr"],
        "Dhuhr": times["dhuhr"],
        "Asr": times["asr"],
        "Maghrib": times["maghrib"],
        "Isha": times["isha"]
    }

def schedule_prayers():
    times = get_today_prayer_times()
    for prayer, time_str in times.items():
        schedule.every().day.at(time_str).do(
            lambda p=prayer: asyncio.create_task(send_prayer_reminder(p))
        )

async def send_prayer_reminder(prayer_name):
    msg = f"🕌 حان الآن وقت صلاة {prayer_name}.\n{prayer_sunnah.get(prayer_name, '')}"
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

# === أوامر البوت ===
async def start(update, context):
    await update.message.reply_text("🌞 بوت ورد كالشمس! يرسل ورد يومي وأذكار وتذكير بالصلاة.")

app.add_handler(CommandHandler("start", start))

# === جدولة ===
def schedule_tasks():
    schedule.every().day.at("06:00").do(lambda: asyncio.create_task(send_daily_ward()))
    schedule.every().day.at("10:00").do(lambda: asyncio.create_task(send_morning_azkar()))
    schedule.every().day.at("17:00").do(lambda: asyncio.create_task(send_evening_azkar()))
    schedule_prayers()

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

# === Flask Web Ping ===
@flask_app.route('/')
def home():
    return "Bot is running ✅"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000)

# === تشغيل البوت ===
async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="✅ البوت شغّال الآن.")
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    threading.Thread(target=run_web).start()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
