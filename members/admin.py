from django.contrib import admin
from .models import Subject, Member, Class as Classe, File

# 1. Define a custom Admin class for Subject
class SubjectAdmin(admin.ModelAdmin):
    # This list determines which columns appear in the admin table
    list_display = ('id', 'name') # Replace 'name'/'created_at' with your actual field names

# 2. Register the model with the custom Admin class
admin.site.register(Subject, SubjectAdmin)

# Register the others normally
admin.site.register(Member)
admin.site.register(Classe)
admin.site.register(File)