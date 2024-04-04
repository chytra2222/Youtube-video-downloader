from django.shortcuts import render
from pytube import YouTube
from downloader.models import Video

def download(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download()
            Video.objects.create(url=url, downloaded=True)
            return redirect('download')
        except Exception as e:
            error_message = "An error occurred during the download process: {}".format(str(e))
            return render(request, 'download.html', {'error_message': error_message})
    videos = Video.objects.all()
    return render(request, 'download.html', {'videos': videos})

def playVideo(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        yt = YouTube(url)
        video = yt.streams.first()
        video_url = video.url
        return render(request, 'play.html', {'video_url': video_url})
