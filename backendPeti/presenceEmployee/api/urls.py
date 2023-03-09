from django.conf.urls import url, include
from .views import PresenceAPIView, PresenceAPIViewID
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', PresenceAPIViewID, basename='employees')
# router.register('percentage-must', PercentageAttendanceAPIView, basename='percentage-must')

urlpatterns = [
    url('presence', PresenceAPIView.as_view()),
    url('', include(router.urls)),
]
