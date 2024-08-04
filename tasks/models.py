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
    current_emotion=models.CharField(max_length=50,blank=True, null=True) #할 일 전 서브 이모션(하나만 선택 가능하게 할 경우)
    changed_emotion=models.CharField(max_length=50,blank=True, null=True) #할 일 마친 후 서브 이모션(하나만 선택 가능하게 할 경우)
    feedback=models.CharField(max_length=200,blank=True,null=True)
    #통계를 위해 추가
    focus_time = models.IntegerField(default=0)  # 초 단위.
    break_time = models.IntegerField(default=0)  # 초 단위.
    #task_emotion = models.TextField(blank=True, null=True)  # 서브 이모션 여러개 선택 가능하게 할 경우 text필드 사용해 리스트 받아오기
