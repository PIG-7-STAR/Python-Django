from django.conf.urls import url, include
from .views import NotesAPIView, NotesAPIVIEWID
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', NotesAPIVIEWID, basename='employee')

urlpatterns = [
    url('list', NotesAPIView.as_view()),
    url('', include(router.urls)),
]