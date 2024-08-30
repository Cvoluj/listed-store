from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

class SMTPMail(models.Model):
    name = models.CharField(max_length=255)
    smtp_server = models.CharField(default='smtp.gmail.com', max_length=255)
    smtp_port = models.IntegerField(default=465)
    smtp_email = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255)
   

    def save(self, *args, **kwargs):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        if self.pk is not None:
            old_instance = SMTPMail.objects.get(pk=self.pk)
            if self.smtp_password != old_instance.smtp_password:
                self.smtp_password = fernet.encrypt(self.smtp_password.encode()).decode()
        else:
            self.smtp_password = fernet.encrypt(self.smtp_password.encode()).decode()

        super().save(*args, **kwargs)

    def decrypt_password(self):
        fernet = Fernet(settings.ENCRYPTION_KEY)
        return fernet.decrypt(self.smtp_password.encode()).decode()

    def __str__(self):
        return self.name
