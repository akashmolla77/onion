from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import os

# --- Environment Variables থেকে টোকেন এবং URL লোড করা হচ্ছে ---
# এই দুটি তথ্য এখন Render-এর Secrets/Environment bölümünden আসবে
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = os.environ.get('WEB_APP_URL')

# --- বটকে ২৪/৭ চালু রাখার জন্য একটি ওয়েব সার্ভার ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running on Render!"

def run():
  # Render PORT পরিবর্তন করতে পারে, তাই os.environ.get ব্যবহার করা হচ্ছে
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

    keyboard = [
        [InlineKeyboardButton("🟢 Open App", web_app={"url": final_web_app_url})],
        [InlineKeyboardButton("💬 Join Community", url="https://t.me/OnionCommunitytg")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ছবির লিংকটিও Environment Variable থেকে নেওয়া যেতে পারে (ঐচ্ছিক)
    photo_url = os.environ.get('WELCOME_PHOTO_URL', "https://i.postimg.cc/0NjyMk7T/20250805-034703.jpg")

    caption_message = (
        f"<b>🎉 Welcome, {user.mention_html()}!</b>\n\n"
        "You've just stepped into <b>ONION Rose BOT</b>, the easiest way to earn money right from your phone.\n\n"
        "<b>Here's what you can do:</b>\n"
        "✅ Watch daily videos for cash.\n"
        "✅ Complete simple tasks.\n"
        "✅ Earn bonuses by referring friends.\n\n"
        "Ready to start? Just click the <b>'Open App'</b> button below!"
    )
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=caption_message,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

def main() -> None:
    # নিশ্চিত করুন যে টোকেন এবং URL লোড হয়েছে
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
