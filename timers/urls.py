from django.urls import path
from . import views

urlpatterns = [
    path('task/<int:task_id>/', views.get_timer_by_task, name='get_timer_by_task'),
]