import os
import random
import re
import string
import phonenumbers
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from healthcare_app.models import Guardian, Patient
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from celery import shared_task
from asgiref.sync import sync_to_async
from phonenumbers import NumberParseException
from telegram import Bot
from telegram import Update,ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from telegram.ext import ContextTypes,MessageHandler,ConversationHandler
from healthcare_app.models import Medication, Frequency
from telegram_bot.models import MedicationReminderForToday,MedicationLog
from telegram_bot.stateConstants import VERIFY_ROLE, VERIFY_CONTACT,VERIFY_UNIQUE_STRING

#WEB VIEWS RELATED TO TELEGRAM BOT
@login_required
@csrf_exempt
def get_unique_string(request):
    user = request.user
    guardian = Guardian.objects.get(UserID=user)
    
    string_exist_in_cache = True
    while string_exist_in_cache:
        letters = ''.join(random.choices(string.ascii_letters, k=7))
        numbers = ''.join(random.choices(string.digits, k=6))
        unique_string = f"{letters}:{numbers}"
        
        # Check if the unique_string already exists in the cache
        if cache.get(unique_string) is None:
            string_exist_in_cache = False
    
    # Expiration time of 2 minutes
    expiration_time = now() + timedelta(minutes=2)
    cache.set(unique_string, guardian.GuardianID, timeout=120)
    print(f"Stored unique string: {unique_string} with Guardian ID: {guardian.GuardianID}")
    
    return JsonResponse(
        {
            "uniqueString": unique_string,
            "expirationTime": expiration_time
        }
    )


#TELEGRAM BOT VIEWS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userName=update.effective_user.first_name
    message = f"Hello {userName}! I am your medication reminder bot. I will help you remember to take your medication on time."
    await update.message.reply_text(text=message)

#VERIFICATION CONVERSATION 
async def start_verification(update,context):
    await update.message.reply_text("Go to the Website settings and click on get unique string to get the unique string and paste it here ")
    return VERIFY_UNIQUE_STRING
    
async def verify_unique_string(update,context):
    unique_string=update.message.text.strip()
    #check if the unique string received from the user is the same as the one stored in the cache. if yes then store the guardian id in the user data
    guardian_id=cache.get(unique_string)
    if guardian_id:
        context.user_data['guardian_id']=guardian_id
        #clear the cache
        cache.delete(unique_string)
        #sending the selection keyboard to user
        reply_keyboard = [['Guardian', 'Patient']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Unique string verified. Please tell if you are a Guardian or a Patient",reply_markup=reply_markup)
        return VERIFY_ROLE
    else:
        await update.message.reply_text("The unique string is invalid or has expired. Please try again.")
        return VERIFY_UNIQUE_STRING
    

async def verify_role(update, context: ContextTypes.DEFAULT_TYPE):
    user_role = update.message.text
    if user_role in ['Guardian', 'Patient']:
        context.user_data['user_role'] = user_role
        contact_keyboard = KeyboardButton(text="Share your contact", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_keyboard]], one_time_keyboard=True)
        await update.message.reply_text("Please share your contact.", reply_markup=reply_markup)
        return VERIFY_CONTACT  # Transition to VERIFY_CONTACT state
    else:
        await update.message.reply_text("Please specify if you are a Guardian or a Patient.")
        return VERIFY_ROLE  # Prompt again for correct input

async def verify_contact(update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    try:
         # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)
        # Get the national (local) number
        local_phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        # Remove any non-digit characters
        local_phone_number = re.sub(r'\D', '', local_phone_number)
        # Remove leading zeroes
        local_phone_number = local_phone_number.lstrip('0')
    except NumberParseException:
        await update.message.reply_text("The phone number you provided is invalid. Please try again.")
        return ConversationHandler.END
    user_role = context.user_data.get('user_role', '')
    try:
        guardian = await sync_to_async(Guardian.objects.get)(GuardianID=context.user_data['guardian_id'])
        if user_role == 'Guardian':
            if guardian.PhoneNumber != local_phone_number:
                await update.message.reply_text("The phone number you provided does not match the guardian. Please try again.")
                return ConversationHandler.END
            guardian.ChatID = update.effective_user.id
            await sync_to_async(guardian.save)()
        elif user_role == 'Patient':
            try:
                patient = await sync_to_async(Patient.objects.get)(GuardianID=guardian, PhoneNumber=local_phone_number)
                patient.ChatID = update.effective_user.id
                await sync_to_async(patient.save)()
            except Patient.DoesNotExist:
                await update.message.reply_text("The phone number you provided does not match the patient. Please try again.")
                return ConversationHandler.END 
        else:
            context.user_data.clear()
            await update.message.reply_text("An error occurred. Please start over.")
            return ConversationHandler.END
    except Guardian.DoesNotExist:
        await update.message.reply_text("Invalid Request. Please try again.")
        return ConversationHandler.END
    
    # Clear user data after processing
    context.user_data.clear()
    await update.message.reply_text("Thank you, your telegram account has been verified.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def cancel(update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # Clear any temporary states or data
    await update.message.reply_text('Operation cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END  # End the conversation

# Send the reminders to the patients about their medication and to the guardians to remind the patients if they haven't taken their medication from the MedicationReminderForToday model
def Send_reminders():
    current_time = timezone.now().time()
    one_hour_earlier_time = (timezone.now() - timedelta(hours=1)).time()
    
    patient_reminders = MedicationReminderForToday.objects.filter(
        NotificationTime__hour=current_time.hour,
        NotificationTime__minute=current_time.minute,
        RemindPatient=True
    )
    
    guardian_reminders = MedicationReminderForToday.objects.filter(
        NotificationTime__hour=one_hour_earlier_time.hour,
        NotificationTime__minute=one_hour_earlier_time.minute,
        RemindGuardian=True,
        isTaken=False
    )
    
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    
    for patient_reminder in patient_reminders:
        message = f"Hello! It's time to take your medication:\nTake {patient_reminder.Dosage} of {patient_reminder.MedicationName} {patient_reminder.Label}"
        try:
            bot.send_message(chat_id=patient_reminder.PatientChatID, text=message)
            #provide a button to mark the medication as taken which stays active for 1 hour
            keyboard = [[KeyboardButton("Mark as taken", callback_data=f"mark_taken_{patient_reminder.MedicationReminderForTodayID}")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            bot.send_message(chat_id=patient_reminder.PatientChatID, text="Did you take your medication?", reply_markup=reply_markup)
        except Exception as e:
            print(f"Failed to send message to patient {patient_reminder.PatientName}: {e}")
    
    for guardian_reminder in guardian_reminders:
        message = f"Your patient {guardian_reminder.PatientName} has to take their medication now. Please remind them."
        try:
            bot.send_message(chat_id=guardian_reminder.GuardianChatID, text=message)
        except Exception as e:
            print(f"Failed to send message to guardian {guardian_reminder.GuardianID}: {e}")



# Get the medication reminders for today with the PatientID, GuardianID, medication name, dosage, and label
def get_medication_reminders_for_today():
    # Add the remaining Medications to the Logs
    all_reminders = MedicationReminderForToday.objects.all()

    for reminder in all_reminders:
        MedicationLog.objects.create(
            GuardianID=reminder.GuardianID,
            PatientID=reminder.PatientID,
            MedicationID=reminder.MedicationID,
            MedicationName=reminder.MedicationName,
            Dosage=reminder.Dosage,
            Label=reminder.Label,
            NotificationTime=reminder.NotificationTime,
            isTaken=reminder.isTaken,
            TimeTaken=reminder.TimeTaken
        )
    
    # Deleting yesterday's data
    MedicationReminderForToday.objects.all().delete()
    
    # Preparing to add today's data
    current_date = timezone.now().date()
    current_day = current_date.strftime("%A")
    medication_ids_for_today = Frequency.get_medication_ids_for_day(current_day)
    
    # Get the medications for today which are active today
    medications = Medication.objects.filter(
        Q(PrescriptionID__PatientID__GuardianID__RemindGuardian=True) |
        Q(PrescriptionID__PatientID__GuardianID__RemindPatient=True),
        MedicationID__in=medication_ids_for_today,
        StartDate__lte=current_date,
        EndDate__gte=current_date,
    ).select_related('PrescriptionID__PatientID__GuardianID').all()
    
    for medication in medications:
        MedicationReminderForToday.objects.create(
            GuardianID=medication.PrescriptionID.PatientID.GuardianID,
            GuardianChatID=medication.PrescriptionID.PatientID.GuardianID.ChatID,
            RemindGuardian=medication.PrescriptionID.PatientID.GuardianID.RemindGuardian,
            RemindPatient=medication.PrescriptionID.PatientID.GuardianID.RemindPatient,
            PatientID=medication.PrescriptionID.PatientID,
            PatientName=medication.PrescriptionID.PatientID.Name,
            PatientChatID=medication.PrescriptionID.PatientID.ChatID,
            MedicationID=medication.MedicationID,
            MedicationName=medication.MedicationName,
            Dosage=medication.Dosage,
            Label=medication.Label,
            NotificationTime=medication.NotificationTime,
        )

#run the function get_medication_reminders_for_today() everyday at 12:00 AM




    


