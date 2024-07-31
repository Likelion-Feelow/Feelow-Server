from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Timers
from .serializers import TimerSerializer

class TimerViewSet(viewsets.ModelViewSet):
    queryset = Timers.objects.all()
    serializer_class = TimerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='create-for-task')
    def create_timer_for_task(self, request):
        task = request.data.get('task')
        emotion = request.data.get('emotion')
        duration = request.data.get('duration')

        if not task or not emotion or not duration:
            return Response({"error": "Task, emotion, and duration are required."}, 
            status=status.HTTP_400_BAD_REQUEST)

        cycle_number = (duration // 1800) + (1 if duration % 1800 != 0 else 0)
        
        if cycle_number > 0:
            focus_time, break_time = self.get_focus_break_time(emotion)
            timer_data = {
                "task": task,
                "emotion": emotion,
                "focus_time": focus_time,
                "break_time": break_time,
                "cycle_number": cycle_number
            }
        else:
            timer_data = {
                "task": task,
                "emotion": emotion,
                "focus_time": duration,
                "break_time": 0,
                "cycle_number": 0
            }

        serializer = TimerSerializer(data=timer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_focus_break_time(self, emotion):
        if emotion in ['기쁨', '희열', '흥분', '행복', '자신감', '열정']:
            return 25 * 60, 5 * 60
        elif emotion in ['안정감', '안도', '휴식', '만족스러움', '차분함']:
            return 20 * 60, 10 * 60
        elif emotion in ['초조함', '걱정', '긴장', '공포', '망설임']:
            return 15 * 60, 15 * 60
        elif emotion in ['두려움', '허무', '실망', '외로움', '후회']:
            return 10 * 60, 20 * 60
        elif emotion in ['짜증', '격분', '불만', '분개', '적대심']:
            return 5 * 60, 25 * 60
        return 25 * 60, 5 * 60
