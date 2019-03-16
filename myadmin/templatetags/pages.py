# -*- coding: utf-8 -*-
# @Time    : 18-9-13 下午2:56
# @Author  : Gold_py
# @Site    : 
# @File    : pages.py
# @Software: PyCharm
from django import template
from django.utils.html import format_html
from myadmin.models import Types
from django.core.urlresolvers import reverse

register = template.Library()
# 自定义乘法计算
@register.simple_tag
def docount(num1,num2):
    return float(num1)*int(num2)



# 头部导航栏
@register.simple_tag
def TopBar():
    # 查询数据
    data = Types.objects.filter(topbar=1)
    # 建立初始html模型
    html = ''
    # 遍历添加
    for ob in data:
        html += '''
        <li class="layout-header-nav-item">
            <a href="{url}" class="layout-header-nav-link">{name}</a>
        </li>
        '''.format(name=ob.name, url=reverse('user_list',args=(ob.id,)))
    return format_html(html)

# 分页标签
@register.simple_tag
def pages(scount, request):
    # 获取关键字查询条件的数据type  和  keyword
    # type = request.GET.type
    # keyword = request.GET.keyword
    data = request.GET.dict()
    u = ''
    for k, v in data.items():
        if not k == 'page':
            u += "&{k}={v}".format(k=k, v=v)

    count = int(scount)
    # 获取当前页面的页码
    p = int(request.GET.get('page', 1))
    # 判断总页码是否小于10
    p = int(p)
    if count <= 10:
        start = 1
        end = count + 1
    else:
        if p <= 6:
            start = 1
        else:
            start = p - 5
        end = start + 10
        if p > count - 4:
            end = count + 1
            start = count - 9
    # 首页 上一页
    if p == 1:
        pgs = '<li><a href="?page=1' + u + '">首页</a></li>' + '<li class="am-disabled"><a href="#">«</a></li>'
    else:
        pgs = '<li><a href="?page=1' + u + '">首页</a></li>' + '<li><a href="?page=             ' + str(
            p - 1) + u + '">«</a></li>'

    for i in range(start, end):
        if p == i:
            print('----------', p)
            print('++++++++++', i)
            pgs += '<li class="am-active"><a href="?page=' + str(i) + u + '">' + str(i) + '</a></li>'
        else:
            pgs += '<li><a href="?page=' + str(i) + u + '">' + str(i) + '</a></li>'
    # 下一页
    if p == count:
        pgs += '<li class="am-disabled"><a href="#">»</a></li>' + '<li><a href="?page=' + str(
            count) + u + '">尾页</a></li>' + '<li>总页数:' + str(count) + '</li>'
    else:
        pgs += '<li><a href="?page=' + str(p + 1) + u + '">»</a></li>' + '<li><a href="?page=' + str(
            count) + u + '">尾页</a></li>' + '<li>总页数:' + str(count) + '</li>'
    return format_html(pgs)



# 自定义隐藏部分手机号的过滤器
@register.filter(name='trans_safe')
def phone_hidden(val):
    oldphone = val
    newphone = oldphone[0:4]+'****'+oldphone[8:]
    return newphone
