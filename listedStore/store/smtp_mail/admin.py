from django.contrib import admin
from .models import SMTPMail

@admin.register(SMTPMail)
class SMTPMailAdmin(admin.ModelAdmin):
    list_display = ('name', 'smtp_server', 'smtp_port', 'smtp_email', 'smtp_password')
