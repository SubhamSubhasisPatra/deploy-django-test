from django.db import models
from django . contrib . auth . models import User
# Create your models here.

class UserProfileInfo(models . Model):

    userInfo = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.userInfo.username