from rest_framework import serializers
from .models import *

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timers
        fields = '__all__'