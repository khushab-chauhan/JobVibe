from django.db import models
from apps.master.models import Baseclass
from apps.users.constant import ACCOUNT_TYPE_CHIOCE, COUSE_CHIOCE
import os

class User(Baseclass):
    account_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE_CHIOCE)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, default='123456')

    def save(self, *args, **kwargs):
        if self.account_type.lower() == 'candidate':
            self.is_active = True
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

def user_profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'user_{instance.user.email}.{ext}'
    return os.path.join('USER_IMAGES/', filename)

def user_resume_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'user_{instance.user.email}.{ext}'
    return os.path.join('USER_RESUMES/', filename)

class User_Personal_Info(Baseclass):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_info")
    profile_picture = models.ImageField(upload_to=user_profile_upload_path, default='DEFAULT_IMAGES/default.jpg', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    course = models.CharField(max_length=255, choices=COUSE_CHIOCE)
    resume = models.FileField(upload_to=user_resume_upload_path)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

