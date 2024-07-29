from django.db import models
from auths.models import CustomUser
# Create your models here.

class Calendars(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    emotion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'date')
