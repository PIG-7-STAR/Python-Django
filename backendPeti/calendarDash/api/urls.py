from django.conf.urls import url, include
from .views import CalendarAPIView, CalendarAPIViewSet, DashboardTopAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee-dashboard', CalendarAPIViewSet, basename='employee-dashboard')
router.register('top-bar', DashboardTopAPIView, basename='top-bar')

urlpatterns = [
    url('off-day', CalendarAPIView.as_view()),
    url('', include(router.urls)),
]
