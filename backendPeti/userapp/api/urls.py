from django.conf.urls import url, include
from .views import UserApiView, UserViewId
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', UserViewId, basename='employee'),

urlpatterns = [
    url('users', UserApiView.as_view()),
    url('', include(router.urls)),
]