from django.conf.urls import url, include
from .views import NotesAPIView, NotesAPIVIEWID, NotesEmployeeCuti
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', NotesAPIVIEWID, basename='employee'),
router.register('employee-cuti', NotesEmployeeCuti, basename='employee-cuti')

urlpatterns = [
    url('list', NotesAPIView.as_view()),
    url('', include(router.urls)),
]