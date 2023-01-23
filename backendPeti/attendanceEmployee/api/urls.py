from django.conf.urls import url, include
from .views import AttendanceAPIView, AttendanceAPIViewID, PercentageAttendanceAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', AttendanceAPIViewID, basename='employees')
router.register('percentage-must', PercentageAttendanceAPIView, basename='percentage-must')

urlpatterns = [
    url('attendance', AttendanceAPIView.as_view()),
    url('', include(router.urls)),
]
