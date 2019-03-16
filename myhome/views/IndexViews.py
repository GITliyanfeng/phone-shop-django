from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Types,Goods


# Create your views here.
# 返回主页面
def homeindex(request):
    # 返回主页面的时候，返回数据
    data2 = Types.objects.filter(level=1)
    data = Types.objects.filter(level=1)
    for i in data:
        i.items = Types.objects.filter(pid=i.id)
    # 展示商品
    goods = Goods.objects.all()
    goods1 = goods[0:5]
    goods2 = goods[5:]
    i = 0
    goods3 = []
    while i<len(goods1):
        goods3.append((goods1[i],goods2[i]))
        i += 1
    print(goods3)
    context = {'Typedata':data,'level2':data2,'good':goods3}
    return render(request,'user/index.html',context)
