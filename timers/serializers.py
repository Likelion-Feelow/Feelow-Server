from rest_framework import serializers
from .models import *

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timers
        fields = '__all__'

class EmotionUpdateSerializer(serializers.Serializer):
    current_emotion = serializers.CharField(max_length=50)

    def update(self, instance, validated_data):
        instance.current_emotion = validated_data.get('emotion', instance.current_emotion)
        instance.save()
        return instance