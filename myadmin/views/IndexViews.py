from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# 返回管理员主页面
def adminindex(request):
    return render(request, 'admin/index.html')

def fileupload(file):
    import time,random
    from web.settings import BASE_DIR
    # 主要是为了形成不会重复的文件名
    filename = str(time.time())+str(random.randint(10000,99999))+'.'+file.name.split('.').pop()
    # 打开文件。写入文件。执行的是文件的上传
    destination = open(BASE_DIR+'/static/pics/'+filename,'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return "/static/pics/"+filename