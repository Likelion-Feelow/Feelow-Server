from django.db import models
from auths.models import CustomUser
from calendars.models import Calendars
# Create your models here.

class Tasks(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    calendar=models.ForeignKey(Calendars,on_delete=models.CASCADE)
    task_name=models.CharField(max_length=100, default='')
    task_description=models.TextField(max_length=500,null=True,blank=True)
    task_duration=models.IntegerField(default=0) #초 단위.
    task_emotion=models.CharField(max_length=50,blank=True, null=True)
    sub_emotion = models.TextField(blank=True, null=True)  # 서브 이모션 필드 추가
