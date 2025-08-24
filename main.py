from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import os

# --- Environment Variables থেকে সমস্ত কনফিগারেশন লোড করা হচ্ছে ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL')
COMMUNITY_URL = os.environ.get('COMMUNITY_URL') # কমিউনিটি লিংকের জন্য নতুন ভেরিয়েবল

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

    # দুটি আলাদা সারিতে বাটন তৈরি করা
    keyboard = [
        [ # প্রথম সারি
            InlineKeyboardButton(
                "🟢 Open App",
                web_app={"url": final_web_app_url}
            )
        ],
        [ # দ্বিতীয় সারি
            InlineKeyboardButton(
                "💬 Join Community",
                url=COMMUNITY_URL  # <-- এখন লিংকটি ভেরিয়েবল থেকে আসছে
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ওয়েলকাম মেসেজ
    welcome_message = (
        f"<b>🎉 Welcome, {user.mention_html()}!</b>\n\n"
        "You've just stepped into <b>ONION Rose BOT</b>, the easiest way to earn money right from your phone.\n\n"
        "<b>Here's what you can do:</b>\n"
        "✅ Watch daily videos for cash.\n"
        "✅ Complete simple tasks.\n"
        "✅ Earn bonuses by referring friends.\n\n"
        "Ready to start? Just click the <b>'Open App'</b> button below!"
    )
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

def main() -> None:
    # নিশ্চিত করুন যে সমস্ত প্রয়োজনীয় ভেরিয়েবল লোড হয়েছে
    if not all([BOT_TOKEN, WEB_APP_URL, COMMUNITY_URL]):
        print("ERROR: One or more environment variables (BOT_TOKEN, WEB_APP_URL, COMMUNITY_URL) are missing!")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    keep_alive()
    main()
