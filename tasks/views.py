import logging
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
import os, openai

logger = logging.getLogger(__name__)
openai.api_key = "sk-None-SMd2TPNVewi3Jrqmn1r3T3BlbkFJcTR0IPMYTPd0yrtGE40m"

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
        logger.error(f"OpenAI API error: {str(e)}")
        return "Error in fetching feedback from ChatGPT."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "An unexpected error occurred."