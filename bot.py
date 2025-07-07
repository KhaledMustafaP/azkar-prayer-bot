import logging
import asyncio
import requests
import nest_asyncio
import schedule
import pytz
from datetime import datetime, timedelta
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
    msg = """☀️ أذكار الصباح كاملة:

أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.
رب أسألك خير ما في هذا اليوم وخير ما بعده، وأعوذ بك من شر ما في هذا اليوم وشر ما بعده.
رب أعوذ بك من الكسل وسوء الكبر، رب أعوذ بك من عذاب في النار وعذاب في القبر.

اللهم بك أصبحنا، وبك أمسينا، وبك نحيا، وبك نموت، وإليك النشور.

اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت، أعوذ بك من شر ما صنعت،
أبوء لك بنعمتك علي، وأبوء بذنبي، فاغفر لي، فإنه لا يغفر الذنوب إلا أنت.

رضيت بالله رباً، وبالإسلام ديناً، وبمحمد ﷺ نبياً.

اللهم إني أصبحت أشهدك وأشهد حملة عرشك، وملائكتك، وجميع خلقك أنك أنت الله لا إله إلا أنت، وحدك لا شريك لك،
وأن محمداً عبدك ورسولك. (أربع مرات)

اللهم ما أصبح بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.

اللهم عافني في بدني، اللهم عافني في سمعي، اللهم عافني في بصري، لا إله إلا أنت. (ثلاث مرات)

اللهم إني أعوذ بك من الكفر والفقر، وأعوذ بك من عذاب القبر، لا إله إلا أنت. (ثلاث مرات)

حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم. (سبع مرات)

اللهم إني أسألك العفو والعافية في الدنيا والآخرة.
اللهم إني أسألك العفو والعافية في ديني ودنياي وأهلي ومالي.
اللهم استر عوراتي، وآمن روعاتي، واحفظني من بين يدي ومن خلفي، وعن يميني وعن شمالي، ومن فوقي،
وأعوذ بعظمتك أن أغتال من تحتي.

يا حي يا قيوم، برحمتك أستغيث، أصلح لي شأني كله، ولا تكلني إلى نفسي طرفة عين.

أصبحنا على فطرة الإسلام، وعلى كلمة الإخلاص، وعلى دين نبينا محمد ﷺ، وعلى ملة أبينا إبراهيم حنيفاً مسلماً، وما كان من المشركين.

سبحان الله وبحمده. (مئة مرة)

لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير. (عشر مرات أو مئة مرة)

أستغفر الله وأتوب إليه. (مئة مرة)

أعوذ بكلمات الله التامات من شر ما خلق. (ثلاث مرات)

بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم. (ثلاث مرات)

قراءة آية الكرسي: ﴿اللّهُ لا إِلَهَ إِلاّ هُوَ الْحَيّ الْقَيّومُ...﴾

وقراءة سور الإخلاص، والفلق، والناس، ثلاث مرات.
"""
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

async def send_evening_azkar():
    msg = """🌙 أذكار المساء كاملة:

أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.
رب أسألك خير ما في هذه الليلة وخير ما بعدها، وأعوذ بك من شر ما في هذه الليلة وشر ما بعدها.
رب أعوذ بك من الكسل وسوء الكبر، رب أعوذ بك من عذاب في النار وعذاب في القبر.

اللهم بك أمسينا، وبك أصبحنا، وبك نحيا، وبك نموت، وإليك المصير.

اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت، أعوذ بك من شر ما صنعت،
أبوء لك بنعمتك علي، وأبوء بذنبي، فاغفر لي، فإنه لا يغفر الذنوب إلا أنت.

رضيت بالله رباً، وبالإسلام ديناً، وبمحمد ﷺ نبياً.

اللهم إني أمسيت أشهدك وأشهد حملة عرشك، وملائكتك، وجميع خلقك أنك أنت الله لا إله إلا أنت، وحدك لا شريك لك،
وأن محمداً عبدك ورسولك. (أربع مرات)

اللهم ما أمسى بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.

اللهم عافني في بدني، اللهم عافني في سمعي، اللهم عافني في بصري، لا إله إلا أنت. (ثلاث مرات)

اللهم إني أعوذ بك من الكفر والفقر، وأعوذ بك من عذاب القبر، لا إله إلا أنت. (ثلاث مرات)

حسبي الله لا إله إلا هو عليه توكلت وهو رب العرش العظيم. (سبع مرات)

اللهم إني أسألك العفو والعافية في الدنيا والآخرة.
اللهم إني أسألك العفو والعافية في ديني ودنياي وأهلي ومالي.
اللهم استر عوراتي، وآمن روعاتي، واحفظني من بين يدي ومن خلفي، وعن يميني وعن شمالي، ومن فوقي،
وأعوذ بعظمتك أن أغتال من تحتي.

يا حي يا قيوم، برحمتك أستغيث، أصلح لي شأني كله، ولا تكلني إلى نفسي طرفة عين.

أمسينا على فطرة الإسلام، وعلى كلمة الإخلاص، وعلى دين نبينا محمد ﷺ، وعلى ملة أبينا إبراهيم حنيفاً مسلماً، وما كان من المشركين.

سبحان الله وبحمده. (مئة مرة)

لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير. (عشر مرات أو مئة مرة)

أستغفر الله وأتوب إليه. (مئة مرة)

أعوذ بكلمات الله التامات من شر ما خلق. (ثلاث مرات)

بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم. (ثلاث مرات)

قراءة آية الكرسي: ﴿اللّهُ لا إِلَهَ إِلاّ هُوَ الْحَيّ الْقَيّومُ...﴾

وقراءة سور الإخلاص، والفلق، والناس، ثلاث مرات.
"""
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

# تذكير بالصيام
async def send_fasting_reminder():
    msg = (
        "🌙 تذكير: صيام الاثنين والخميس سنة عن النبي ﷺ\n\n"
        "قال رسول الله ﷺ:\n"
        "«تُعرض الأعمال يوم الاثنين والخميس فأحب أن يُعرض عملي وأنا صائم»\n\n"
        "🔖 فاحرص على الصيام إن استطعت."
    )
    await app.bot.send_message(chat_id=CHAT_ID, text=msg)

def schedule_fasting_reminders():
    schedule.every().sunday.at("17:00").do(lambda: asyncio.create_task(send_fasting_reminder()))
    schedule.every().wednesday.at("17:00").do(lambda: asyncio.create_task(send_fasting_reminder()))

# مواقيت الصلاة
def get_today_prayer_times():
    url = f"https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method=99&fajr=18&isha=18"
    response = requests.get(url)
    data = response.json()

    if data['code'] != 200:
        return None

    timings = data['data']['timings']

    return {
        "Fajr": timings['Fajr'],
        "Sunrise": timings['Sunrise'],
        "Dhuhr": timings['Dhuhr'],
        "Asr": timings['Asr'],
        "Maghrib": timings['Maghrib'],
        "Isha": timings['Isha']
    }

async def send_prayer_times():
    times = get_today_prayer_times()
    if not times:
        await app.bot.send_message(chat_id=CHAT_ID, text="❌ فشل في جلب مواقيت الصلاة.")
        return

    message = "🕌 مواقيت الصلاة اليوم في عمّان:\n"
    message += f"📿 الفجر: {times['Fajr']}\n"
    message += f"🌅 الشروق: {times['Sunrise']}\n"
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

# ضبط التوقيت من عمّان إلى UTC
def adjust_time_to_utc(time_str):
    jordan_time = datetime.strptime(time_str, "%H:%M")
    adjusted_time = jordan_time - timedelta(hours=3)
    return adjusted_time.strftime("%H:%M")
async def send_jumuah_sunnah():
    msg = (
        "🕌 *سنن يوم الجمعة*\n\n"
        "1️⃣ الاغتسال والتطيب.\n"
        "2️⃣ التبكير إلى صلاة الجمعة.\n"
        "3️⃣ قراءة سورة الكهف.\n"
        "4️⃣ الإكثار من الصلاة على النبي ﷺ.\n"
        "5️⃣ الدعاء في الساعة الأخيرة قبل المغرب.\n\n"
        "🤍 جمعة مباركة!"
    )
    await app.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

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
        utc_time = adjust_time_to_utc(time_str)
        schedule.every().day.at(utc_time).do(create_reminder_task(prayer)).tag('prayers')

# أوامر البوت
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
    schedule.every().day.at("07:00").do(lambda: asyncio.create_task(send_morning_azkar()))
    schedule.every().day.at("16:00").do(lambda: asyncio.create_task(send_evening_azkar()))
    schedule.every().day.at("00:01").do(schedule_prayer_reminders)
    schedule.every().friday.at("06:00").do(lambda: asyncio.create_task(send_jumuah_sunnah()))

    schedule_prayer_reminders()
    schedule_fasting_reminders()

# السيرفر للفحص
@flask_app.route('/')
def home():
    return "✅ البوت يعمل"

def run_web():
    flask_app.run(host="0.0.0.0", port=10000)

# التشغيل
async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

async def main():
    await app.bot.send_message(chat_id=CHAT_ID, text="✅ تم تشغيل البوت.")
    schedule_tasks()
    asyncio.create_task(scheduler_loop())
    threading.Thread(target=run_web).start()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
