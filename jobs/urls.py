# home/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('career/', views.career, name='career'), 
]
