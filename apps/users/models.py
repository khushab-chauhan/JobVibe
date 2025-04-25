from django.db import models
from apps.master.models import Baseclass
from apps.users.constant import ACCOUNT_TYPE_CHIOCE
# Create your models here.

class User(Baseclass):
    account_type = models.CharField(max_length=255,choices=ACCOUNT_TYPE_CHIOCE,blank=False,null=False) 
    email = models.EmailField(max_length=255,unique=True,blank=False,null=False)
    password = models.CharField(max_length=255,blank=False,null=False)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=10,default='123456')

    def save(self,*args,**kwargs):
        if self.account_type.lower() == 'candidate':
            self.is_active = True
        super(User,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.email

