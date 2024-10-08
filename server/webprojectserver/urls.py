from django.contrib import admin
from django.urls import path
from auth_app.views import login_view, signup_view, logout_view, check_login
from healthcare_app.views import  add_guardian, update_guardian, view_guardian,get_guardian_notification_status,set_guardian_notification_status
from healthcare_app.views import add_patient,view_patients,delete_patients_all
from healthcare_app.views import view_prescriptions ,add_prescription
from telegram_bot.views import get_unique_string
from file_handler.views import download_patient,initiate_patient_upload,upload_patient_chunk,complete_patient_upload


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('check_login/', check_login, name='check_login'),
    path('guardian/add/', add_guardian, name='add_guardian'),
    path('guardian/update/', update_guardian, name='update_guardian'),
    path('guardian/view/', view_guardian, name='view_guardian'),
    path('guardian/notification/status/', get_guardian_notification_status, name='get_guardian_notification_status'),
    path('guardian/notification/status/set/', set_guardian_notification_status, name='set_guardian_notification_status'),
    path('patient/download/',download_patient, name='download_patient'),
    path('patient/upload/initiate/', initiate_patient_upload, name='initiate_patient_upload'),
    path('patient/upload/chunk/', upload_patient_chunk, name='upload_patient_chunk'),
    path('patient/upload/complete/', complete_patient_upload, name='complete_patient_upload'),
    path('patient/add/', add_patient, name='add_patient'),
    path('patient/view/', view_patients, name='view_patients'),
    path('patient/delete/all/', delete_patients_all, name='delete_patients_all'),
    path('prescription/view/<int:patient_id>/', view_prescriptions, name='view_prescriptions'),
    path('prescription/add/<int:patient_id>/', add_prescription, name='add_prescription'),
    path('telegram/unique_string/', get_unique_string, name='get_unique_string'),
]
