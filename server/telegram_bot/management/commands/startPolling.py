from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler
import os

from telegram_bot.views import start

class Command(BaseCommand):
    help = 'Starts the bot in polling mode.'

    def handle(self, *args, **options):
        application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        
        # Add handlers
        application.add_handler(CommandHandler('start', start))

        # Start polling
        self.stdout.write(self.style.SUCCESS('Successfully starting bot in polling mode.'))
        application.run_polling()
        
        
        