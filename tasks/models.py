from django.db import models
from auths.models import CustomUser
from calendars.models import Calendars
# Create your models here.

class Tasks(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    calendar=models.ForeignKey(Calendars,on_delete=models.CASCADE)
    task_name=models.CharField(max_length=100),
    task_description=models.TextField(max_length=500,null=True,blank=True),
    task_duration=models.IntegerField #분단위.
    task_emotion=models.CharField(max_length=50,blank=True, null=True)