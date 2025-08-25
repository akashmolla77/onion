 # --- Environment Variables থেকে সমস্ত কনফিগারেশন লোড করা হচ্ছে ---
 BOT_TOKEN = os.environ.get('BOT_TOKEN')
 WEB_APP_URL = os.environ.get('WEB_APP_URL')
 COMMUNITY_URL = os.environ.get('COMMUNITY_URL')
 WELCOME_PHOTO_URL = os.environ.get('WELCOME_PHOTO_URL')

 async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     user = update.effective_user
     args = context.args
     
     final_web_app_url = WEB_APP_URL
     if args:
         referral_code = args[0]
         final_web_app_url += f"?ref={referral_code}"

     keyboard = [
         [InlineKeyboardButton("🟢 Open App", web_app={"url": final_web_app_url})],
         [InlineKeyboardButton("💬 Join Community", url=COMMUNITY_URL)]
     ]
     reply_markup = InlineKeyboardMarkup(keyboard)

     caption_message = (
         f"<b>🎉 Welcome, {user.mention_html()}!</b>\-n\-"
         "You've just stepped into <b>ONION Rose BOT</b>, the easiest way to earn money right from your phone.\-n\-"
         "<b>Here's what you can do:</b>\n"
         "✅ Watch daily videos for cash.\n"
         "✅ Complete simple tasks.\n"
         "✅ Earn bonuses by referring friends.\n\n"
         "Ready to start? Just click the <b>'Open App'</b> button below!"
     )
     
     await context.bot.send_photo(
         chat_id=update.effective_chat.id,
         photo=WELCOME_PHOTO_URL,
         caption=caption_message,
         reply_markup=reply_markup,
         parse_mode='HTML'
     )

 def main() -> None:
     # নিশ্চিত করুন যে সমস্ত ভেরিয়েবল লোড হয়েছে
     if not all([BOT_TOKEN, WEB_APP_URL, COMMUNITY_URL, WELCOME_PHOTO_URL]):
         print("CRITICAL ERROR: One or more required environment variables are missing!")
         return
         
     application = Application.builder().token(BOT_TOKEN).build()
     application.add_handler(CommandHandler("start", start))
     
     print("Bot is running successfully on Railway...")
     application.run_polling()

 if __name__ == "__main__":
     main()
 ```
