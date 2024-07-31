from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimerViewSet

router = DefaultRouter()
router.register(r'timers', TimerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
