from django.urls import path
from video.views import (
    new_release_video,
    detail_video_view
)


app_name = 'video'

urlpatterns = [
    path('', new_release_video, name='video_home'),
    path('detail/<int:my_id>', detail_video_view, name='detail_video')
]