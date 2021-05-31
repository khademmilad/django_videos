from django.shortcuts import get_object_or_404, render
from video.models import Video, Subscriber
from django.http import HttpResponse


def new_release_video(request):
    try:
        queryset = Video.objects.all()
    except:
        return HttpResponse('Something went wrong!')
        
    dic = {
        'queryset' : queryset
    }
    return render(request, 'video/new_release_video.html', dic)
    
    

def detail_video_view(request, my_id):
    video = get_object_or_404(Video, pk=my_id)
    
    count_likes = video.count_likes()
    
    video.video_views = video.video_views + 1
    video.save()
    
    dic = {
        'video' : video,
        'count_likes' : count_likes,
    }
    return render(request, 'video/detail_video.html', dic)
    
