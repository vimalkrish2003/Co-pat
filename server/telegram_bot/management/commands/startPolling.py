from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
import os
from telegram_bot.stateConstants import VERIFY_ROLE, VERIFY_CONTACT,VERIFY_UNIQUE_STRING
from telegram_bot.views import start,start_verification,verify_unique_string,verify_role, verify_contact, cancel



class Command(BaseCommand):
    help = 'Starts the bot in polling mode.'

    def handle(self, *args, **options):
        application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

        # Conversational Handler
        mobile_verification_handler = ConversationHandler(
            entry_points=[CommandHandler('verify', start_verification)],
            states={
                VERIFY_UNIQUE_STRING: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_unique_string)],
                VERIFY_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_role)],
                VERIFY_CONTACT: [MessageHandler(filters.CONTACT, verify_contact)],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        # Add handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(mobile_verification_handler)

        # Start polling
        self.stdout.write(self.style.SUCCESS('Successfully starting bot in polling mode.'))
        application.run_polling()