from django.conf.urls import url, include
from .views import Login
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

urlpatterns = [
    url('auth', Login.as_view(), name='auth'),
    # url('', include(router.urls)),
]