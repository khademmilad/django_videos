from django.urls import path
from video.views import (
    new_release_video,
)


app_name = 'video'

urlpatterns = [
    path('', new_release_video, name='video_home')
]