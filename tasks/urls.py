from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.create_and_get_task),
    path('<int:id>',views.delete_task_and_choice_emotion),
    #path('feedback/<int:id>', views.get_feedback, name='get_feedback'),
]