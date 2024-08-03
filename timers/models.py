from django.db import models
from tasks.models import Tasks

class Timers(models.Model):
    task = models.ForeignKey(Tasks,on_delete = models.CASCADE)
    emotion = models.CharField(max_length = 50,blank = True, null = True)
    focus_time = models.IntegerField(default = 25 * 60)
    break_time = models.IntegerField(default = 5 * 60)  # focus + break = 30분, 가중치는 Tasks.emotions 마다 상이 
    cycle_number = models.IntegerField(default = 1)

    def __str__(self):
        return self.name