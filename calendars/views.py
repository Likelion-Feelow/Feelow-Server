from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Calendars
#from tasks.models import Tasks
from .serializers import CalendarSerializer
from rest_framework import serializers,status
#from tasks.serializers import TaskSerializer
from datetime import datetime, timedelta, date
import calendar

# Create your views here.

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
    all_dates = [{'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'), 'emotion': None} for i in range((end_date - start_date).days + 1)]
    
    # Retrieve calendar entries for the given month 
    calendars = Calendars.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
    for calendar_entry in calendars:
        for date_info in all_dates:
            if date_info['date'] == calendar_entry.date.strftime('%Y-%m-%d'):
                date_info['emotion'] = calendar_entry.emotion
                break
            
    #데이터 베이스에 저장.      
    for date_info in all_dates:
        if not Calendars.objects.filter(user=user,date=date_info['date']):
            Calendars.objects.create(user=user,date=date_info['date'],emotion=None)
    
    ## 할일에 대한 시리얼라이저, tasks 구현 후 주석처리 풀기
    today = datetime.today().date()
    #today_tasks = Tasks.objects.filter(user=user, calendar__date=today)
    #today_task_serializer = TaskSerializer(today_tasks, many=True)
    
    response_data = {
        "calendars": all_dates,  # Include all dates in the response
        #"today_tasks": today_task_serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
