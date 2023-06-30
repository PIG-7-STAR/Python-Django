from django.contrib import admin
from django.urls import path, include
from noteHR.api.views import get_cuti
from userapp.api import views
from attendanceEmployee.api.views import AttendanceAPISearch, TopAttendanceAPIView, AttendanceAPICompare, AttendanceAPIAnalisis
from userapp.api.views import EmployeeBirth, UserSearch, UserSearchView, UserPasswordReset, ResetPassword, UserSearchContract, UserWorkHourAPIView, EmployeeContractEnd, ChangePasswordAPIView
from calendarDash.api.views import WeekTotals, post_delete_calendar
from presenceEmployee.api.views import PresenceAPIAnalisis, PresenceAPICompare, PresenceSearch, TopPresenceAPIView, PresenceStatistikUser, StatistikPresenceInMonth, StatistikSubmissionEmployeeInMonth
from submisssion.api.views import    CalendarSubmissionView, SubmissionIzin, send_notification_api
from noteHR.api.views import post_delete_notes

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
    path('users/employee-total/<int:year>', views.UserTotal.as_view()),
    path('users/employee/cuti/<int:emp_id>/<int:year>/', get_cuti ),
    path('users/employee/change-password/', ChangePasswordAPIView.as_view()), 
    
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
    path('api/presence/total-day/', TopPresenceAPIView.as_view()),

    path('api/note/', include('noteHR.api.urls')),
    path('api/note/delete/', post_delete_notes),

    path('api/dashboard/', include('calendarDash.api.urls')),
    path('api/dashboard/week-of', WeekTotals.as_view()),
    path('api/dashboard/day-of/delete/', post_delete_calendar),
    path('api/dashboard/employee-permission/', SubmissionIzin.as_view()),
    path('api/employee/best_of/', UserWorkHourAPIView.as_view()),
    path('api/dashboard/employee-birth/<int:month>/', EmployeeBirth.as_view()),
    path('api/dashboard/contract-end/<int:month>/<int:year>/', EmployeeContractEnd.as_view()),
    path('api/dashboard/statistik-presence/<int:year>/', StatistikPresenceInMonth.as_view()),
    path('api/dashboard/statistik-submission/<int:year>/', StatistikSubmissionEmployeeInMonth.as_view()),
    path('api/dashboard/employee-statistik/<int:month>/<int:year>/', PresenceStatistikUser.as_view()),

    path('api/submission/', include('submisssion.api.urls')),
    path('api/submission/calendar', CalendarSubmissionView.as_view()),
    
    path('api/send-notification/', send_notification_api, name='send_notification'),

]
