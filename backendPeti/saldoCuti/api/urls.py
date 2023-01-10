from django.conf.urls import url, include
from .views import SaldoApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url('user/sisa-cuti', SaldoApiView.as_view()),
    url('', include(router.urls)),
]