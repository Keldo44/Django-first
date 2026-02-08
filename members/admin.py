from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import Subject,Member,Class as Classe

# Registras cada uno para que Django los pinte en el panel
admin.site.register(Member)
admin.site.register(Subject)
admin.site.register(Classe)
