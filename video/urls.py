from os import name
from django.urls import path
from video.views import (
    new_release_video,
    detail_video_view,
    like_view,
    sub_add,
    upload_video,
)


app_name = 'video'

urlpatterns = [
    path('', new_release_video, name='video_home'),
    path('detail/<int:my_id>', detail_video_view, name='detail_video'),
    path('like/<int:pk>', like_view, name="like_video"),
    path('subscribe/<int:my_id>', sub_add, name="subscribe"),
    path('upload-video/', upload_video, name='uplaod_video'),
    
]