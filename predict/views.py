from django.shortcuts import render, HttpResponse
from project import settings
import os
from predict.model import pred

# Create your views here.
def index(request):
    if request.method == 'GET':
        for f in os.scandir(settings.MEDIA_ROOT):
            os.remove(f.path)
        return render(request, 'predict/index.html')
        
    elif request.method == 'POST':
        # request.FILES.getlist("파라미터이름") : 여러개의 파일을 list 저장
        # request.FILES.get("파라미터이름") : 한개의 파일을 가져오기
        filename = request.FILES.get("files")

        uploadfile = open(settings.MEDIA_ROOT.joinpath(str(filename)), 'wb')
        for chunk in filename.chunks():
            uploadfile.write(chunk)

        result = pred.predmain(str(filename))

        context = {
            "result" : result
        }

        return render(request, 'predict/index.html', context)

def download(request, filename):
    #filename='duke2.png'

    filepath = settings.MEDIA_ROOT.joinpath(filename)

    readfile = open(filepath, 'rb')
    response = HttpResponse(readfile.read())

    response['Content-Disposition']='attachment;filename='+os.path.basename(filepath)
    response['Content-type']='image/png'

    return (response)

def downlist(request):
    dirlist = os.listdir(settings.MEDIA_ROOT)
    context = {
        'dirlist' : dirlist,
    }
    return render(request, 'predict/downlist.html', context)