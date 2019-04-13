from django.urls import path
from . import views

urlpatterns = [
    path('video_captions/', views.video_captions, name="video_captions"),
]