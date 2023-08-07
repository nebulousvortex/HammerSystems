from django.db import models

class Users(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)
    referral_code = models.CharField(max_length=6, null=True, blank=True)

