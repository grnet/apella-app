from django.contrib import admin
from .models import ApellaUser, Position, Candidacy

admin.site.register(ApellaUser)
admin.site.register(Position)
admin.site.register(Candidacy)
