from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tasks, Timers, Emotions
from .serializers import EmotionUpdateSerializer#, TaskSerializer, TimerSerializer
import requests

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'], url_path='update-emotion')
    def update_emotion(self, request, pk=None):
        task = self.get_object()
        serializer = EmotionUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 타이머 생성 로직
            timer_data = self.create_timer_data(task)
            timer_response = requests.post(
                "http://your_timer_service_url/timers/", 
                json=timer_data, 
                headers={"Authorization": f"Bearer {request.auth}"}
            )
            if timer_response.status_code == 201:
                return Response(timer_response.json(), status=status.HTTP_201_CREATED)
            else:
                return Response(timer_response.json(), status=timer_response.status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_timer_data(self, task):
        emotion = task.task_emotion
        duration = task.task_duration
        cycle_number = (duration // 1800) + (1 if duration % 1800 != 0 else 0)

        if cycle_number > 0:
            focus_time, break_time = self.get_focus_break_time(emotion)
            return {
                "task": task.id,
                "emotion": emotion,
                "focus_time": focus_time,
                "break_time": break_time,
                "cycle_number": cycle_number
            }
        else:
            return {
                "task": task.id,
                "emotion": emotion,
                "focus_time": duration,
                "break_time": 0,
                "cycle_number": 0
            }

    def get_focus_break_time(self, emotion):
        if emotion in Emotions.HAPPY:
            return 25 * 60, 5 * 60
        elif emotion in Emotions.CALM:
            return 20 * 60, 10 * 60
        elif emotion in Emotions.DEPRESSED:
            return 15 * 60, 15 * 60
        elif emotion in Emotions.ANXIETY:
            return 10 * 60, 20 * 60
        elif emotion in Emotions.ANGER:
            return 5 * 60, 25 * 60
        return 25 * 60, 5 * 60