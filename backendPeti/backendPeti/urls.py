from django.contrib import admin
from django.urls import path, include
from userapp.api import views
from attendanceEmployee.api.views import AttendanceAPISearch, TopAttendanceAPIView, AttendanceAPICompare
from userapp.api.views import UserSearch, UserSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('', include('loginUser.api.urls')),
    path('petitions/', include('pengajuanEmp.api.urls')),
    path('notes/', include('notes.api.urls')),
    path('users/', include('userapp.api.urls')),
    path('users/employee/search/', UserSearch.as_view()),
    path('users/employee/name/', UserSearchView.as_view()),
    path('users/employee-total/', views.UserTotal.as_view()),
    path('cuti/', include('saldoCuti.api.urls')),
    path('attendance/', include('attendanceEmployee.api.urls')),
    path('attendance/employee-sea/', AttendanceAPISearch.as_view()),
    path('attendance/employee/compare/', AttendanceAPICompare.as_view()),
    path('attendance/total-day/', TopAttendanceAPIView.as_view()),
    path('dashboard/', include('calendarDash.api.urls')),
]
