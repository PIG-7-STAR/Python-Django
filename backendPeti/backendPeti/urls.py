from django.contrib import admin
from django.urls import path, include
from userapp.api import views
from attendanceEmployee.api.views import AttendanceAPISearch, TopAttendanceAPIView, AttendanceAPICompare, AttendanceAPIAnalisis
from userapp.api.views import UserSearch, UserSearchView, UserPasswordReset, ResetPassword, UserSearchContract, UserWorkHourAPIView
from calendarDash.api.views import WeekTotals
from presenceEmployee.api.views import PresenceAPIAnalisis, PresenceAPICompare, PresenceSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/reset-password/', UserPasswordReset.as_view(), name='reset-password'),
    path('api/reset-password/<str:encoded_pk>/<str:token>/',ResetPassword.as_view(), name='reset-password'),
    path('', include('loginUser.api.urls')),
    path('petitions/', include('pengajuanEmp.api.urls')),
    path('notes/', include('notes.api.urls')),
    path('users/', include('userapp.api.urls')),
    path('users/employee/search/', UserSearch.as_view()),
    path('users/employee/contract/', UserSearchContract.as_view()),
    path('users/employee/name/', UserSearchView.as_view()),
    path('users/employee-total/', views.UserTotal.as_view()),
    path('cuti/', include('saldoCuti.api.urls')),
    path('attendance/', include('attendanceEmployee.api.urls')),
    path('attendance/employee-sea/', AttendanceAPISearch.as_view()),
    path('attendance/employee-analysis/', AttendanceAPIAnalisis.as_view()),
    path('attendance/employee/compare/', AttendanceAPICompare.as_view()),
    path('attendance/total-day/', TopAttendanceAPIView.as_view()),

    path('api/presence/', include('presenceEmployee.api.urls')),
    path('api/presence/employee/search', PresenceSearch.as_view()),
    path('api/presence/employee/compare', PresenceAPICompare.as_view()),
    path('api/presence/employee/analysis/', PresenceAPIAnalisis.as_view()),

    path('api/note/', include('noteHR.api.urls')),

    path('api/dashboard/', include('calendarDash.api.urls')),
    path('api/dashboard/week-of', WeekTotals.as_view()),

    path('api/submission/', include('submisssion.api.urls')),

    path('api/employee/best_of/', UserWorkHourAPIView.as_view()),


]
