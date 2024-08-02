from rest_framework import serializers
from auths.models import CustomUser
from calendars.models import Calendars
from .models import Tasks

class ViewTaskSerializer(serializers.ModelSerializer):
    date=serializers.DateField(source='calendar.date')
    
    class Meta:
        model = Tasks
        fields = ["id","date","task_name","task_duration","current_emotion","changed_emotion"]
        
        
        
class TaskSerializer(serializers.ModelSerializer):
    calendar_id = serializers.PrimaryKeyRelatedField(source='calendar', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    task_id = serializers.IntegerField(source='id', read_only=True)
    
    class Meta:
        model = Tasks
        fields = ["task_id", "calendar_id", "user_id", "task_name", "task_duration", "task_description"]

        
class CreateTaskSerializer(serializers.ModelSerializer):
    date = serializers.DateField(write_only=True)
    
    class Meta:
        model=Tasks
        #fields=["user","date","calendar","task_name","task_duration","task_description"]
        fields = ["date", "task_name", "task_duration", "task_description"]
        
        
    def create(self,validated_data):
        user = self.context['request'].user
        date=validated_data.pop('date')
        #calendar=Calendars.objects.get(user=user,date=date)
        calendar, created = Calendars.objects.get_or_create(user=user, date=date)
        validated_data['user']=user
        validated_data['calendar']=calendar
        return Tasks.objects.create(**validated_data)
    
    
class EmotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ["task_name", "current_emotion", "changed_emotion"]