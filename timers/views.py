from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Timers
from tasks.models import Tasks

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timer_by_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
#     emotion = task.current_emotion
#     duration = task.task_duration

#     focus_time, break_time, cycle_number = calculate_timer(duration, emotion)

#     timer_data = {
#         "task": task.id,
#         "emotion": emotion,
#         "focus_time": focus_time,
#         "break_time": break_time,
#         "cycle_number": cycle_number
#     }

#     return Response(timer_data, status=status.HTTP_200_OK)

# def calculate_timer(duration, emotion):
#     if emotion in Emotions.HAPPY:
#         focus_time, break_time = 25 * 60, 5 * 60
#     elif emotion in Emotions.CALM:
#         focus_time, break_time = 20 * 60, 10 * 60
#     elif emotion in Emotions.ANXIETY:
#         focus_time, break_time = 15 * 60, 15 * 60
#     elif emotion in Emotions.DEPRESSED:
#         focus_time, break_time = 10 * 60, 20 * 60
#     elif emotion in Emotions.ANGER:
#         focus_time, break_time = 5 * 60, 25 * 60
#     else:  # default (Pomodoro)
#         focus_time, break_time = 25 * 60, 5 * 60

#     cycle_number = (duration // 1800) + (1 if duration % focus_time != 0 else 0)
#     return focus_time, break_time, cycle_number
