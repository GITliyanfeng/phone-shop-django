from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .TypeViews import SelectAndOrder
from django.core.urlresolvers import reverse
from ..models import Goods,Types
from django.db.models import Q
from web.settings import BASE_DIR
import os
from django.contrib.auth.decorators import permission_required


# Create your views here.


def fileupload(file):
    import time,random
    from web.settings import BASE_DIR
    # 主要是为了形成不会重复的文件名
    filename = str(time.time())+str(random.randint(10000,99999))+'.'+file.name.split('.').pop()
    # 打开文件。写入文件。执行的是文件的上传
    destination = open(BASE_DIR+'/static/pics/goodsimg/'+filename,'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return "/static/pics/goodsimg/"+filename

# 商品列表的显示
@permission_required('myadmin.select_good',raise_exception=True)
def adminlistgoods(request):
    # 获取所有数据
    data = Goods.objects.exclude(status=3)
    # 关键字查询和分页
    type = request.GET.get('type', 'all')
    keyword = request.GET.get('keyword', '')
    # 通过关键字查询字段  Q 查询
    if type == 'all':
        data = data.filter(Q(name__contains=keyword) | Q(tid__name__contains=keyword) | Q(price__contains=keyword) | Q(num__contains=keyword))
    else:
        info = {type + '__contains': keyword}
        data = data.filter(**info)

    # 数据分页
    # 实例化分页对象，参数1，数据列表，每页显示的条数
    p = Paginator(data, 10)
    # 获取当前的页码数
    pages = request.GET.get('page', 1)
    # 获取当前页的数据
    userlist = p.page(pages)
    # 获取所有页码的列表
    # pages = p.page_range
    # 分配数据
    context = {'data': userlist}
    # 解析模板
    return render(request,'admin/goods/listgoods.html',context)

# 商品 的添加---返回表单页面
@permission_required('myadmin.create_good',raise_exception=True)
def adminaddgoods(request):
    # 分配选择所属分类部分的数据
    data = SelectAndOrder()
    context = {"data":data}
    return render(request,'admin/goods/add.html',context)


# 商品 的添加
@permission_required('myadmin.create_food',raise_exception=True)
def admininsertgoods(request):
    try:
        # 获取页面中的数据
        data = request.POST.dict()
        # 去除验证信息
        data.pop('csrfmiddlewaretoken')
        # 判断是否上传了图片
        mypic = request.FILES.get('pic',None)
        # 如果没有上传图片，返回添加页面，提示，必须上传图片
        if not mypic:
            return HttpResponse('<script>alert("必须上传商品图片");location.href="'+reverse("admin_add_goodss")+'"</script>')
        pic = fileupload(mypic)
        data['pic'] = pic
        data['tid'] = Types.objects.get(id=data['tid'])
        print(data)
        Goods.objects.create(**data)
        return HttpResponse('<script>alert("添加成功");location.href="' + reverse('admin_list_goods') + '"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="' + reverse('admin_add_goods') + '"</script>')


# ajax 删除商品
@permission_required('myadmin.remove_good',raise_exception=True)
def admindeletegoods(request):
    try:
        id = request.GET['id']
        # 获取对象
        ob = Goods.objects.get(id=id)
        if ob:
            ob.status=3
        ob.save()
        return JsonResponse({'error':0,'msg':'删除成功'})
    except:
        return JsonResponse({'error':1,'msg':'删除失败'})


# 编辑----返回form表单
@permission_required('myadmin.remake_good',raise_exception=True)
def admindeitgoods(request,id):
    # 分类信息
    types = SelectAndOrder()
    data = Goods.objects.get(id=id)
    context = {'data':data,'types':types}
    return render(request,'admin/goods/edit.html',context)


# 编辑----提交编辑后的数据
@permission_required('myadmin.remake_good',raise_exception=True)
def adminupdategoods(request):
    try:
        # 获取提交的数据
        data = request.POST.dict()
        # 去除验证信息
        ob = Goods.objects.get(id=data['id'])
        data.pop('csrfmiddlewaretoken')
        old = ob.pic
        # 判断是否上传了图片
        mypic = request.FILES.get('pic', None)
        # 判断图片是否更改了
        if mypic:
            # print(mypic)
            # 删除原来的图片
            os.remove(BASE_DIR+old)
        #     # 上传新的图片
            pic = fileupload(mypic)
            data['pic'] = pic
        #     # data['tid'] = Types.objects.get(id=data['tid'])
        else:
            data['pic'] = old
        ob.info = data['info']
        ob.name = data['name']
        ob.pic = data['pic']
        ob.status = data['status']
        ob.pic = data['pic']
        ob.save()
        return HttpResponse('<script>alert("修改成功");location.href="' + reverse('admin_list_goods') + '"</script>')
    except:
        return HttpResponse('<script>alert("修改失败");location.href="' + reverse('admin_add_goods') + '"</script>')

