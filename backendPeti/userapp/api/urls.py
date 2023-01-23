from django.conf.urls import url, include
from .views import UserApiView, UserViewId, UserRole, UserDivisionView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', UserViewId, basename='employees'),
router.register('employees-roles', UserRole, basename='employees-roles'),
router.register('employees-division', UserDivisionView, basename='employees-division'),

urlpatterns = [
    url('users', UserApiView.as_view()),
    url('', include(router.urls)),
]