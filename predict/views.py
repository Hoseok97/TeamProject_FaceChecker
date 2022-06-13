from django.shortcuts import render, HttpResponse
from project import settings
import os
from predict.model import pred
from predict import detect

# Create your views here.
def index(request):
    if request.method == 'GET':
        for f in os.scandir(settings.MEDIA_ROOT):
            os.remove(f.path)
        for g in os.scandir(settings.BASE_DIR/ 'static/detect'):
            os.remove(g.path)
        return render(request, 'predict/index.html')      
    elif request.method == 'POST':
        # request.FILES.getlist("파라미터이름") : 여러개의 파일을 list 저장
        # request.FILES.get("파라미터이름") : 한개의 파일을 가져오기
        filename = request.FILES.get("files") # 이게.?? 2진? 음?허?
        

        ## 파일 하나만인데

        
        uploadfile = open(settings.MEDIA_ROOT.joinpath(str(filename)), 'wb') ## media 파일 생성
       
        for chunk in filename.chunks(): ## 이게 머하는 부분이지?  

            uploadfile.write(chunk) ## 실제 파일 작성

        
        # 1. -> 업로드한 이미지만 처리해야함  
        # -> 
        # 2. -> 결과값을 화면에 출력해야함 (ok)

        ## 2-1. -> 잘됨, 잘못됨 판단 
        ## 2-2. -> 잘되었을 때
        ## 2-3. -> 잘못되었을 때
        

        # ex1. 결과로 뱉으면 -> images 폴더 내용 전부 삭제 또는 다른 곳으로 이동
        # ex1-2 - > 다른 곳으로 이동하는 경우 데이터 누적해서 학습시키기 위해서

        # 화면 출력 어떡해?

        # 이건..강제적으로 해야함...
        # output 내놓는건.. 우리의 .. 사명인데....



        result = detect.run()
        
        print("클래스이름 : ", result[0])
        print("저장된 전체 경로 : ", result[1])
        print("저장된 파일 이름 : ", result[2])
             
        context = {
             "result" : result[0],
             "fileName" : result[2],
         }
        if result[0] == 'safe':
            return render(request, 'predict/safe.html', context)      
        else: 
            return render(request, 'predict/notsafe.html', context)
       
        

        


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