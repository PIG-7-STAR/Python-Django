from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('', include('loginUser.api.urls')),
    # path('first-app/', include('fistApp.api.urls')),
    path('petitions/', include('pengajuanEmp.api.urls')),
    path('notes/', include('notes.api.urls')),
    path('users/', include('userapp.api.urls')),
    path('cuti/', include('saldoCuti.api.urls')),
]
