from rest_framework import serializers
from collections import Counter
from .models import Tasks, Calendars
from .emotions import Emotions

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
        calendar, created = Calendars.objects.get_or_create(user=user, date=date)
        validated_data['user']=user
        validated_data['calendar']=calendar
        return Tasks.objects.create(**validated_data)
    
    
class EmotionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ["task_name", "current_emotion", "changed_emotion"]

    def update(self, instance, validated_data):
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.current_emotion = validated_data.get('current_emotion', instance.current_emotion)
        instance.changed_emotion = validated_data.get('changed_emotion', instance.changed_emotion)
        instance.save()
        self.update_superior_emotion(instance.calendar)
        return instance

    def update_superior_emotion(self, calendar):
        tasks_for_day = Tasks.objects.filter(user=calendar.user, calendar=calendar, current_emotion__isnull=False).exclude(current_emotion='')
        # Print current_emotion for debugging
        print("Tasks and Emotions:")
        for task in tasks_for_day:
            print(f"Task: {task.task_name}, Emotion: {task.current_emotion}")

        emotion_categories = [Emotions.get_emotion_category(task.current_emotion) for task in tasks_for_day if task.current_emotion]
        
        # Print emotion categories for debugging
        print(f"Emotion Categories: {emotion_categories}")

        if emotion_categories:
            emotion_counts = Counter(emotion_categories)
            most_common_emotion, _ = emotion_counts.most_common(1)[0]
            # Print most common emotion for debugging
            print(f"Most Common Emotion: {most_common_emotion}")
            calendar.superior_emotion = most_common_emotion
        else:
            calendar.superior_emotion = None
        calendar.save()