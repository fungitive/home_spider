from django.urls import path
from . import views

urlpatterns = [
    path('start', views.get_url, name='get_url'),
    ]