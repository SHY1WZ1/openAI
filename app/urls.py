from django.urls import path
from . import views


urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('modify/<int:file_id>/', views.modify_file, name='modify_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]
