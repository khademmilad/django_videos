from django.shortcuts import render
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
    
