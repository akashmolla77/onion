 # --- আপনার বটের টোকেন এবং Web App-এর লিংক এখানে দিন ---
 BOT_TOKEN = "7587712501:AAHrh9Dm4zUZO5E76JAQlQ4snOGZ0Krw4Tg" # আপনার আসল বট টোকেন
 WEB_APP_URL = "https://tgminingbot.blogspot.com/" # আপনার ব্লগস্পট লিংক

 # --- বটকে ২৪/৭ চালু রাখার জন্য একটি ওয়েব সার্ভার ---
 app = Flask('')

 @app.route('/')
 def home():
     return "Bot is alive and running on Render!"

 def run():
   app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

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

     caption_message = (
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
         text=caption_message,
         reply_markup=reply_markup,
         parse_mode='HTML',
         disable_web_page_preview=True
     )

 def main() -> None:
     application = Application.builder().token(BOT_TOKEN).build()
     application.add_handler(CommandHandler("start", start))
     print("Bot is running...")
     application.run_polling()

 if __name__ == "__main__":
     keep_alive()
     main()
 ```