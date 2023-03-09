from django.conf.urls import url, include
from .views import NotesAPIView, NotesAPIVIEWID
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee-notes', NotesAPIVIEWID, basename='employee-notes'),

urlpatterns = [
    url('list-notes', NotesAPIView.as_view()),
    url('', include(router.urls)),
]