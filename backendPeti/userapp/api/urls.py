from django.conf.urls import url, include
from .views import UserApiView, UserViewId, UserRole
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', UserViewId, basename='employees'),
router.register('employees-roles', UserRole, basename='employees-roles'),

urlpatterns = [
    url('users', UserApiView.as_view()),
    url('', include(router.urls)),
]