from django.conf.urls import url, include
from .views import SubmissionAPIView, SubmissionAPIViewID, SubmissionCalendarAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', SubmissionAPIViewID, basename='employees')
router.register('employees-calendar', SubmissionCalendarAPI, basename='employees-calendar')

urlpatterns = [
    url('submission', SubmissionAPIView.as_view()),
    url('', include(router.urls)),
]