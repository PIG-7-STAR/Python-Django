from django.conf.urls import url, include
from .views import fistFunction
from rest_framework.routers import DefaultRouter
from .views import PengajuansViewset

router = DefaultRouter()
router.register('pengajuan-emp', PengajuansViewset, basename='pengajuan-emp')

urlpatterns = [
    url('fist', fistFunction),
    url('', include(router.urls))
]