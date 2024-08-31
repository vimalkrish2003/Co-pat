from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from telegram_bot.views import get_medication_reminders_for_today

class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(get_medication_reminders_for_today, 'cron', hour=0, minute=0)
        scheduler.start()