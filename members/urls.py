from zipfile import Path

from django.urls import path
from . import views

urlpatterns = [
    path('horari/tarde', views.horari_tarde),
    path('', views.horari),
    path('file', views.get_txt_file),
    path('file/upload/', views.upload_file),
    path('files/list', views.files_list),
    path('files/<int:file_id>', views.file_detail, name='file_detail'),
]