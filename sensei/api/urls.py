from django.urls import path, include
from . import views
from rest_framework import routers, viewsets
from api.views import *

urlpatterns = [
    path('', views.upload_files, name='upload_files'),
    path('download/', views.download_result, name='download_result')
]