from django.contrib import admin
from .models import DomesticProfessor, ForeignProfessor

#admin.site.register(UserProfile)
admin.site.register(DomesticProfessor)
admin.site.register(ForeignProfessor)
