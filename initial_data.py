import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from timers.models import Timers

Timers.objects.create(emotion = "happy", focus_time = 3600, break_time = 1200, cycle_number = 3)
Timers.objects.create(emotion = "happy", focus_time = 1000, break_time = 200, cycle_number = 2)
Timers.objects.create(emotion = "sad", focus_time = 400, break_time = 200, cycle_number = 1)
Timers.objects.create(emotion = "sad", focus_time = 2030, break_time = 600, cycle_number = 5)
Timers.objects.create(emotion = "anxiety", focus_time = 1000, break_time = 100, cycle_number = 3)
Timers.objects.create(emotion = "anxiety", focus_time = 1400, break_time = 3000, cycle_number = 2)
Timers.objects.create(emotion = "anxiety", focus_time = 400, break_time = 100, cycle_number = 9)