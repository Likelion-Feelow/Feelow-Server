from rest_framework import serializers
from .models import *

class TimerSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(source='task', read_only=True)
    
    class Meta:
        model = Timers
        fields = ["id", "task_id", "emotion", "focus_time", "break_time", "cycle_number"]

    def create(self, validated_data):
        return Timers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.emotion = validated_data.get('emotion', instance.emotion)
        instance.focus_time = validated_data.get('focus_time', instance.focus_time)
        instance.break_time = validated_data.get('break_time', instance.break_time)
        instance.cycle_number = validated_data.get('cycle_number', instance.cycle_number)
        instance.save()
        return instance