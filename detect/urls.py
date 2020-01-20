from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.Streaming.home),
        path('check', views.Streaming.load),
        path('detect/', views.Streaming.detect),
        path('golive/', views.Streaming.go_live),
        path('download/', views.Streaming.download),
]
