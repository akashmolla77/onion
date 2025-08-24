from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import os

# --- Environment Variables থেকে টোকেন এবং URL লোড করা হচ্ছে ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL')

# --- বটকে ২৪/৭ চালু রাখার জন্য একটি ওয়েব সার্ভার ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running on Render!"

def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    args = context.args
    
    final_web_app_url = WEB_APP_URL
    if args:
        referral_code = args[0]
        final_web_app_url += f"?ref={referral_code}"

    # শুধুমাত্র একটি বাটন তৈরি করা হচ্ছে
    keyboard = [
        [
            InlineKeyboardButton(
                "🟢 Open App & Start Earning!",
                web_app={"url": final_web_app_url}
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # নতুন এবং সংক্ষিপ্ত ওয়েলকাম মেসেজ
    welcome_message = (
        f"<b>🎉 Welcome, {user.mention_html()}!</b>\n\n"
        "Welcome to <b>ONION 🟢™</b>, the easiest way to earn money right from your phone.\n\n"
        "Ready to start your earning journey? Click the button below to launch the app!"
    )
    
    # মেসেজ এবং বাটন পাঠানো হচ্ছে
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

def main() -> None:
    if not BOT_TOKEN or not WEB_APP_URL:
        print("ERROR: BOT_TOKEN or WEB_APP_URL not found in environment variables!")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    keep_alive()
    main()

