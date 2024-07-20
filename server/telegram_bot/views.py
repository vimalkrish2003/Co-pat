import os
from telegram import Update
from telegram.ext import ContextTypes
from healthcare_app.models import Medication

#create a greeting while starting the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userName=update.effective_user.first_name
    message = f"Hello {userName}! I am your medication reminder bot. I will help you remember to take your medication on time."
    await update.message.reply_text(text=message)

# implement a reminder function send a notification to the patients mobile number on the notification time for that medication if that day is set as true in the Frequency table and is between the start date and end date. It should be efficient and industry standard

    
    


