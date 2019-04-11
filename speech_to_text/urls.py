from django.urls import path
from . import views

urlpatterns = [
    path('convert_video/', views.convert_video, name="convert_video"),
]