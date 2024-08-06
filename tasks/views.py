from rest_framework.status import HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from calendars.models import Calendars
from tasks.models import Tasks
from calendars.serializers import CalendarSerializer
from rest_framework import serializers,status
from .serializers import *
from datetime import datetime, timedelta, date
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import os
from auths.models import CustomUser
import calendar, requests

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_and_get_task(request):
    print("Authorization Header:", request.headers.get('Authorization'))  # 헤더 출력
    print("User:", request.user)
    
    user=request.user
    today=date.today()
    
    if request.method == 'POST':
        serializer = CreateTaskSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            task = serializer.save()
            response_serializer = TaskSerializer(task)
            response_data = response_serializer.data
            return Response(response_data, status=201)        
        return Response(serializer.errors, status=400)

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        
        if year and month and day:
            try:
                target_date = date(int(year), int(month), int(day))
            except ValueError:
                return Response({"error": "잘못된 형식입니다."}, status=400)
        else:
            target_date = today
        tasks = Tasks.objects.filter(user=user, calendar__date=target_date)
        serializer = ViewTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)

@api_view(['DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def delete_task_and_choice_emotion(request, id):
    task = get_object_or_404(Tasks, id=id)
    
    if request.method == 'DELETE':
        calendar = task.calendar
        task.delete()
        EmotionUpdateSerializer().update_superior_emotion(calendar)  # 작업 삭제 후 superior_emotion 업데이트
        return Response(status=204)

    if request.method == 'PATCH':
        serializer = EmotionUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
''' 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feedback(request, id):
    task = get_object_or_404(Tasks, id=id)
    emotion = task.current_emotion
    task_name = task.task_name
    if not emotion:
        return Response({"error": "Task has no current emotion set."}, status=400)
    feedback = get_chatgpt_feedback(task_name, emotion)
    return Response({"feedback": feedback}, status=200)

def get_chatgpt_feedback(task_name, emotion):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide feedback based on the user's emotion."},
                {"role": "user", "content": f"You have completed your task which is {task_name} while feeling {emotion}. Please provide feedback in less than 300 characters in Korean."}
            ]
        )
        feedback = completion.choices[0].message.content.strip()
        return feedback
    except openai.OpenAIError as e:
        return "Error in fetching feedback from ChatGPT."
    except Exception as e:
        return "An unexpected error occurred."
        
'''
#통게를 위해 추가

#통계는 '오늘'이 아닌 전날까지의 데이터만 통계에 포함됨.
#예를들어 오늘이 8월 6일이면 8월의 통계는 8월1일~8월5일까지의 데이터만 포함되는 결과임. 
from .serializers import TaskStatisticsSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_statistics(request):
    user = request.user  # 현재사용자
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    day = int(request.GET.get('day'))

    target_date = date(year, month, day)
    tasks = Tasks.objects.filter(user=user, calendar__date=target_date) #현재 사용자 구별 위해 추가
    total_focus_time = sum(task.focus_time * task.cycle_count for task in tasks if task.cycle_count is not None)
    total_break_time = sum(task.break_time * task.cycle_count for task in tasks if task.cycle_count is not None)
    
    
    emotions = [task.current_emotion for task in tasks] + [task.changed_emotion for task in tasks]
    emotion_categories = [Emotions.get_emotion_category(emotion) for emotion in emotions if emotion]
    emotion_counts = Counter(emotion_categories)
    
    # 현재 사용자의 닉네임을 가져옵니다.
    user = request.user
    nickname = user.nickname  # CustomUser 모델에서 닉네임 필드를 가져옵니다.


    data = {
        'nickname': nickname,
        'total_focus_time': total_focus_time,
        'total_break_time': total_break_time,
        'emotion_counts': dict(emotion_counts)
    }

    serializer = TaskStatisticsSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)