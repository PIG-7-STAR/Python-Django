from django.contrib import admin
from .models import Petitions, PetitionsCalendar

admin.site.register(Petitions)
admin.site.register(PetitionsCalendar)