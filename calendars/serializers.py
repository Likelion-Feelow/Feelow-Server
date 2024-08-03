from rest_framework import serializers
from auths.models import CustomUser
from .models import Calendars

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendars
        fields = ['user', 'date', 'superior_emotion']