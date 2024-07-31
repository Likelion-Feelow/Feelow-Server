from rest_framework.status import HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from calendars.models import Calendars
from tasks.models import Tasks
from calendars.serializers import CalendarSerializer
from rest_framework import serializers,status
from .serializers import ViewTaskSerializer,CreateTaskSerializer,TaskSerializer,EmotionUpdateSerializer
from datetime import datetime, timedelta, date
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import calendar
import requests
# Create your views here.

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_and_get_task(request):
    user=request.user
    today=date.today()
    
    if request.method == 'POST':
        serializer = CreateTaskSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            task = serializer.save()
            #return Response(serializer.data, status=201)
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        '''
        if year and month and day:
            target_date = date(int(year), int(month), int(day))
            tasks = Tasks.objects.filter(user=user, calendar__date=target_date)
        else:
            tasks = Tasks.objects.filter(user=user, calendar__date=date.today())
        
        serializer = ViewTaskSerializer(tasks, many=True)
        '''
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
        task.delete()
        return Response(status=204)

    if request.method == 'PATCH':
        serializer = EmotionUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
            

def get_chatgpt_feedback(emotion):
    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer YOUR_OPENAI_API_KEY",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-davinci-003",
        "prompt": f"You have completed your task while feeling {emotion}. Please provide a feedback in less than 200 characters with Korean.",
        "max_tokens": 100,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        feedback = response.json()['choices'][0]['text'].strip()
        return feedback
    else:
        return "Error in fetching feedback from ChatGPT."
