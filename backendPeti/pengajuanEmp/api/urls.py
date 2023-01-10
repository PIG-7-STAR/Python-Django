from django.conf.urls import url, include
from .views import PengajuanAPIView, PengajuanAPIViewID, PengajuanCalendarAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', PengajuanAPIViewID, basename='employee')
router.register('employee-calendar', PengajuanCalendarAPI, basename='employee-calendar')

urlpatterns = [
    url('pengajuan', PengajuanAPIView.as_view()),
    url('', include(router.urls)),
]