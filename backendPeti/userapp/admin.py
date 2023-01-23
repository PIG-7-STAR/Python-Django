from django.contrib import admin
from .models import User, UserRoles, UserDivision

admin.site.register(User)
admin.site.register(UserRoles)
admin.site.register(UserDivision)

