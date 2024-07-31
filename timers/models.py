from django.db import models
from tasks.models import Tasks

class Emotions():
    HAPPY = ['기쁨', '희열', '흥분', '행복', '자신감', '열정'] # 5:1 - 5/6
    CALM = ['안정감', '안도', '휴식','만족스러움', '차분함'] # 2:1 - 2/3
    DEPRESSED = ['초조함', '걱정', '긴장', '공포', '망설임'] # 1:1 - 1/2
    ANXIETY = ['두려움', '허무', '실망', '외로움', '후회'] # 1:1 - 1/2
    ANGER = ['짜증', '격분', '불만', '분개', '적대심'] # 1:3 - 1/4

class Timers(models.Model):
    task = models.ForeignKey(Tasks,on_delete = models.CASCADE)
    emotion = models.CharField(max_length = 50,blank = True, null = True)
    focus_time = models.IntegerField(default = 25 * 60)
    break_time = models.IntegerField(default = 5 * 60)  # focus + break = 30분, 가중치는 Tasks.emotions 마다 상이 
    cycle_number = models.IntegerField(default = 1)

    def __str__(self):
        return self.name