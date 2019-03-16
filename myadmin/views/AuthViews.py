# -*- coding: utf-8 -*-
# @Time    : 18-9-25 下午5:54
# @Author  : Gold_py
# @Site    : 
# @File    : AuthViews.py
# @Software: PyCharm
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import permission_required


# 解析管理员的登录页面
def AdminLogin(request):
    return render(request, 'admin/adminlogin.html')


# 执行管理员登录的验证
def CheckAdmin(request):
    admin_data = request.POST.dict()
    username = admin_data['username']
    password = admin_data['password']
    # django认证登录
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponse('<script>alert("登录成功");location.href="' + reverse('admin_index') + '"</script>')
    else:
        return HttpResponse('<script>alert("用户名或者密码错误，登录失败");location.href="' + reverse('admin_login') + '"</script>')


# 管理员登出
def AdminLogout(request):
    logout(request)
    return HttpResponse('<script>alert("管理员登出");location.href="' + reverse('admin_login') + '"</script>')


# 添加管理员
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthAddUser(request):
    try:
        group_data = Group.objects.all()
        context = {'data': group_data}
        if request.method == 'GET':
            return render(request, 'admin/auth/user/add.html', context)
        elif request.method == 'POST':
            grouplist = request.POST.getlist('prms', None)
            data = request.POST.dict()
            print(data['level'],'++++++++',type(data['level']))
            # 判断选择的管理员的等级
            if data['level'] == '1':
                # 超级管理
                ob = User.objects.create_superuser(data['name'], data['email'], data['password'])
            else:
                # 普通管理
                ob = User.objects.create_user(data['name'], data['email'], data['password'])
            # 判断是否分配组
            if group_data:
                ob.groups.set(grouplist)
                ob.save()
        return HttpResponse('<script>alert("创建管理员成功");location.href="' + reverse('auth_list_user') + '"</script>')
    except:
        return HttpResponse('<script>alert("创建管理员失败");location.href="' + reverse('auth_add_user') + '"</script>')


# 管理员用户的列表
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthListUser(request):
    data = User.objects.all()
    context = {'data': data}
    return render(request, 'admin/auth/user/list.html', context)


# 管理员的删除
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthDelUser(request):
    try:
        id = request.GET['id']
        ob = User.objects.get(id=id)
        ob.delete()
        return HttpResponse('<script>alert("删除管理员成功");location.href="' + reverse('auth_list_user') + '"</script>')
    except:
        return HttpResponse('<script>alert("删除管理员失败");location.href="' + reverse('auth_list_user') + '"</script>')


# 用户组的管理
# 添加用户组
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthAddGroup(request):
    # 将所有自定义的权限信息查询出来
    data = Permission.objects.all().exclude(name__istartswith='can')
    context = {'data': data}
    if request.method == 'GET':
        return render(request, 'admin/auth/group/add.html', context)
    elif request.method == 'POST':
        try:
            # 执行添加组的过程
            group_name = request.POST['name']
            g = Group(name=group_name)
            g.save()
            group_prms = request.POST.getlist('prms', None)
            # print(group_prms)
            # 判断是否为组添加了权限
            if group_prms:
                g.permissions.set(group_prms)
                g.save()
            return HttpResponse('<script>alert("创建权限组成功");location.href="' + reverse('auth_list_group') + '"</script>')
        except:
            return HttpResponse('<script>alert("创建权限组失败");location.href="' + reverse('auth_add_group') + '"</script>')


# 权限组的列表
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthListGroup(request):
    data = Group.objects.all().order_by('id')
    context = {'data': data}
    return render(request, 'admin/auth/group/list.html', context)


# 权限组的跟改
@permission_required('myadmin.is_superuser',raise_exception=True)
def AuthEditGroup(request):
    id = request.GET['id']
    if request.method == 'GET':
        group_data = Group.objects.get(id=id)
        context = {'group_data': group_data}
        prms_left = Permission.objects.exclude(name__istartswith='can').exclude(group=group_data)
        prms_right = Permission.objects.exclude(name__istartswith='can').filter(group=group_data)
        context['data_left'] = prms_left
        context['data_right'] = prms_right
        return render(request, 'admin/auth/group/edit.html', context)
    elif request.method == 'POST':
        try:
            data = request.POST.dict()
            ob = Group.objects.get(id=data['id'])
            ob.name = data['name']
            ob.permissions.clear()
            ob.save()
            prms = request.POST.getlist('prms', None)
            if prms:
                ob.permissions.set(prms)
                ob.save()
            return HttpResponse('<script>alert("修改权限组成功");location.href="' + reverse('auth_list_group') + '"</script>')
        except:
            return HttpResponse('<script>alert("修改权限组失败");location.href="' + reverse('auth_list_group') + '"</script>')
