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

    all_dates = []
    calendars = Calendars.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
    today = datetime.today().date()
    today_tasks = Tasks.objects.filter(user=user, calendar__date=today)
    today_task_serializer = TaskSerializer(today_tasks, many=True)


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
