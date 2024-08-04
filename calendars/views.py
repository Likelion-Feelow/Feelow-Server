from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Calendars
from tasks.models import Tasks
from rest_framework import status
from tasks.serializers import TaskSerializer
from datetime import datetime, timedelta, date
from collections import Counter
import calendar

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_calendar(request):
    user = request.user
    year = request.GET.get('year')
    month = request.GET.get('month')
    year = int(year)
    month = int(month)
    start_date = date(year, month, 1)
    end_date = date(year, month, calendar.monthrange(year, month)[1])
    
    # 각 달의 모든 날들에 대한 리스트 생성
    #all_dates = [{'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'), 'superior_emotion': None} for i in range((end_date - start_date).days + 1)]
                
    # for date_info in all_dates:
    #     if not Calendars.objects.filter(user=user,date=date_info['date']).exists():
    #         Calendars.objects.create(user=user, date=date_info['date'], superior_emotion=None)
   
    # Retrieve calendar entries for the given month 
    all_dates = []
    calendars = Calendars.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
    # for calendar_entry in calendars:
    #         tasks_for_day = Tasks.objects.filter(user=user, calendar__date=date_info['date'])
    #         emotions = [task.current_emotion for task in tasks_for_day if task.current_emotion]
        
    #         if emotions:
    #             emotion_counts = Counter(emotions)
    #             most_common_emotion, _ = emotion_counts.most_common(1)[0]
    #             calendar_entry = Calendars.objects.get(user=user, date=date_info['date'])
    #             calendar_entry.superior_emotion = most_common_emotion
    #             calendar_entry.save()
    #         else: #task가 없을 경우 
    #             calendar_entry = Calendars.objects.get(user=user, date=date_info['date'])
    #             calendar_entry.superior_emotion = None
    #             calendar_entry.save()
 
    today = datetime.today().date()
    today_tasks = Tasks.objects.filter(user=user, calendar__date=today)
    today_task_serializer = TaskSerializer(today_tasks, many=True)
    
    # response_data = {
    #     "calendars": all_dates,  # Include all dates in the response
    #     "today_tasks": today_task_serializer.data
    # }

    for calendar_entry in calendars:
            all_dates.append({
                'date': calendar_entry.date.strftime('%Y-%m-%d'),
                'superior_emotion': calendar_entry.superior_emotion
            })

    response_data = {
        "calendars": all_dates,
        "today_tasks": today_task_serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
