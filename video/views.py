from account.models import Account
from django.shortcuts import get_object_or_404, redirect, render
from video.models import Video, Subscriber
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import UpdateView


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
    
    is_liked = False
    if video.likes.filter(id = request.user.id).exists():
        is_liked = True
    
    video.video_views = video.video_views + 1
    video.save()
    
    account = video.user
    
    is_self = True
    user = request.user
    
    if user.is_authenticated and user != account:
        is_self = False
    elif not user.is_authenticated:
        is_self = False
    
    dic = {
        'video' : video,
        'count_likes' : count_likes,
        'is_liked' : is_liked,
        'is_self' : is_self
    }
    return render(request, 'video/detail_video.html', dic)
    
    

def like_view(request, pk):
    video = get_object_or_404(Video, id=request.POST.get('video_id'))
    Liked = False
    if video.likes.filter(id = request.user.id).exists():
        video.likes.remove(request.user)
        Liked = False
    else:
        video.likes.add(request.user)
        Liked = True
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


def sub_add(request, my_id):
    profile_to_subscribe = Subscriber.objects.get_or_create(user = Account.objects.get(id = my_id))[0]
    
    subscriber = Account.objects.get(pk = request.user.id)
    
    subscribed = False
    if subscriber in profile_to_subscribe.subscribers.all():
        profile_to_subscribe.subscribers.remove(subscriber)
        subscribed = True
    else:
        profile_to_subscribe.subscribers.add(subscriber)
        subscribed = False
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

def upload_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        video_file =  request.FILES['fileName']
        user_obj = request.user
        upload_video = Video(user=user_obj, title=title, desc=desc, video_file=video_file)
        upload_video.save()
        
        return redirect('video:video_home')
        
    return render(request, 'video/upload_video.html')
    
    
def my_videos(request):
    context = {}
    user_id = request.user.id
    my_videos = Video.objects.filter(user__id = user_id).order_by('pup_date')
    
    context = {
        'my_videos' : my_videos
    }
    
    return render(request, 'video/my_videos.html', context)
    
    
def delete_video(request, my_id):
    video = get_object_or_404(Video, pk=my_id)
    if request.method == 'POST':
        video.delete()
    
    return HttpResponseRedirect(reverse('video:my_videos'))
    
    
class Updatevideo(UpdateView):
    model = Video
    template_name = 'video/edit-video.html'
    fields = ['title', 'desc']
    
    def get_success_url(self):
        return reverse('video:my_videos')