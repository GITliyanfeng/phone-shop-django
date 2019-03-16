# -*- coding: utf-8 -*-
# @Time    : 18-9-23 下午2:34
# @Author  : Gold_py
# @Site    : 
# @File    : AdminLoginMiddleware.py
# @Software: PyCharm
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import re


class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # 检测当前的请求是否已经登录,如果已经登录,.则放行,如果未登录,则跳转到登录页
        # 获取当前用户的请求路径  /admin/开头  但不是 /admin/login/  /admin/dologin/   /admin/verifycode
        # 定义可以访问的路由
        adminurllist = [
            reverse('admin_login'),
            reverse('check_admin'),
        ]
        if re.match('/myadmin/',request.path) and request.path not in adminurllist:

            if not request.session.get('_auth_user_id',None):
                print(request.session.get('_auth_user_id'))
                return HttpResponse('<script>alert("请先登录");location.href="'+reverse('admin_login')+'"</script>')


        lastpath = request.GET
        keys = '?'
        valus = ''
        for k, v in lastpath.items():
            keys += k
            valus += v
        homeurllist = [
            reverse('order_make'),
            reverse('order_create'),
            reverse('order_pay_for'),
            reverse('order_pay_for_suscess'),
            reverse('my_order_list'),
            reverse('add_address'),
            reverse('my_center'),
        ]
        # 判断当前是否进入前台，如果进入前台，以及request.path请求属于定义的列表之中，那么将进行登录认证
        if request.path in homeurllist:
            # 检测session中是否有VipUser的记录
            if request.session.get('VipUser', '') == '':
                return HttpResponse('<script>alert("请先登录");location.href="' + reverse(
                    'user_login') + '?lastpath=' + request.path + keys + '=' + valus + '";</script>')

        response = self.get_response(request)
        return response
