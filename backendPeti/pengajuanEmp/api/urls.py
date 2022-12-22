from django.conf.urls import url, include
from .views import PengajuanAPIView, PengajuanAPIViewID
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', PengajuanAPIViewID, basename='employee')

urlpatterns = [
    url('pengajuan', PengajuanAPIView.as_view()),
    url('', include(router.urls)),
]