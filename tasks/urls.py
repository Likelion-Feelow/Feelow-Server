from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.create_and_get_task),
    path('<int:id>',views.delete_task_and_choice_emotion),
    # path('<int:id>/feedback', views.get_feedback),
]