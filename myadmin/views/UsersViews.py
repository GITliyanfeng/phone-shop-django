from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .IndexViews import fileupload
import os
from web.settings import BASE_DIR
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

from ..models import Users


# Create your views here.
# 添加会员的操作一，返回表单页面
@permission_required('myadmin.create_user', raise_exception=True)
def adminadduser(request):
    return render(request, 'admin/user/adduser.html')


# 添加会员提交数据
@permission_required('myadmin.create_user', raise_exception=True)
def admincreateuser(request):
    try:
        date = request.POST.dict()
        date.pop('csrfmiddlewaretoken')
        # 密码要经过加密的处理
        date['password'] = make_password(date['password'], None, 'pbkdf2_sha256')
        # 获取上传文件信息，判断是否有文件被上传过
        print(date)
        myfile = request.FILES.get('pic', None)
        print(myfile)
        if myfile:
            from .IndexViews import fileupload
            filename = fileupload(myfile)
            date['pic'] = filename
            print(date)
        else:
            date['pic'] = '/static/pics/default.jpg'
        Users.objects.create(**date)
        return HttpResponse('<script>alert("添加成功");location.href="' + reverse('admin_list_user') + '"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="' + reverse('admin_add_user') + '"</script>')


# 列出用户
@permission_required('myadmin.select_user', raise_exception=True)
def adminlistuser(request):
    data = Users.objects.exclude(statu=2)

    # 分类查询
    # 获取页面提交过来的类型和检索关键字
    type = request.GET.get('type', 'all')
    keyword = request.GET.get('keyword', '')
    # 通过关键字查询字段  Q 查询
    if type == 'all':
        data = data.filter(Q(username__contains=keyword) | Q(email__contains=keyword) | Q(age__contains=keyword) | Q(
            phone__contains=keyword))
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

    context = {'data': userlist}
    return render(request, 'admin/user/listuser.html', context)


# 删除用户
@permission_required('myadmin.remove_user', raise_exception=True)
def admindeluser(request, id):
    try:
        ob = Users.objects.get(id=id)
        ob.statu = 2
        ob.save()
        return HttpResponse('<script>alert("删除成功");location.href="' + reverse('admin_list_user') + '"</script>')
    except:
        return HttpResponse('<script>alert("删除失败");location.href="' + reverse('admin_list_user') + '"</script>')
@permission_required('myadmin.emake_user', raise_exception=True)
def adminstopuser(request,id):
    try:
        ob = Users.objects.get(id=id)
        ob.statu = 1
        ob.save()
        return HttpResponse('<script>alert("禁用成功");location.href="' + reverse('admin_list_user') + '"</script>')
    except:
        return HttpResponse('<script>alert("禁用失败");location.href="' + reverse('admin_list_user') + '"</script>')


# 更改
@permission_required('myadmin.remake_user', raise_exception=True)
def adminedituser(request, id):
    # 获取对象
    data = Users.objects.get(id=id)
    # 分配数据
    context = {'data': data}
    # 解析模板
    return render(request, 'admin/user/edit.html', context)


@permission_required('myadmin.remake_user', raise_exception=True)
def adminupdateuser(request):
    # 获取网页数据
    try:
        data = request.POST.dict()
        # 生成对象
        ob = Users.objects.get(id=data['id'])
        ob.username = data['username']
        ob.age = data['age']
        ob.sex = data['sex']
        ob.email = data['email']
        ob.phone = data['phone']
        if not data['password'] == '':
            ob.password = make_password(data['password'], None, 'pbkdf2_sha256')
        # 判断是否更改头像
        myfile = request.FILES.get('pic', None)
        if myfile:
            # 判断原来的头像是否是默认的头像
            if not ob.pic == '/static/pics/default.jpg':
                # 删除旧的图片
                os.remove(BASE_DIR + ob.pic)
            filename = fileupload(myfile)
            data['pic'] = filename
            ob.pic = data['pic']
        ob.save()
        lastpath = request.GET.get('space', None)
        if not lastpath:
            return HttpResponse('<script>alert("跟改成功");location.href="' + reverse('admin_list_user') + '"</script>')
        else:
            return HttpResponse('<script>alert("跟改成功");location.href="' + lastpath + '"</script>')
    except:
        lastpath = request.GET.get('space', None)
        if not lastpath:
            return HttpResponse('<script>alert("跟改失败");location.href="' + reverse('admin_list_user') + '"</script>')
        else:
            return HttpResponse('<script>alert("跟改失败");location.href="' + lastpath + '"</script>')
