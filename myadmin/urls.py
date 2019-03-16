# -*- coding: utf-8 -*-
# @Time    : 18-9-12 下午1:47
# @Author  : Gold_py
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import IndexViews,UsersViews,TypeViews,GoodsViews,OrderViews,AuthViews


urlpatterns = [
    # 访问管理员路由，返回管理员主页面
    url(r'^$',IndexViews.adminindex,name='admin_index'),
    # 管理员的登录页面
    url('^user/adminlogin',AuthViews.AdminLogin,name='admin_login'),
    # 管理员登出页面
    url('^urer/adminloginout',AuthViews.AdminLogout,name='admin_logout'),
    # 执行管理员登录的验证
    url('^user/checkadmin',AuthViews.CheckAdmin,name='check_admin'),
    # 添加表单页面
    url(r'^user/adduser/$',UsersViews.adminadduser,name='admin_add_user'),
    # 创建对象，插入到数据库
    url(r'^user/createuser/$',UsersViews.admincreateuser,name='admin_create_user'),
    # 列出所有用户
    url(r'^user/listuser/$',UsersViews.adminlistuser,name='admin_list_user'),
    # 逻辑删除
    url(r'^user/deluser/(?P<id>[0-9]+)/$',UsersViews.admindeluser,name='admin_del_user'),
    # 禁用
    url(r'^user/Stopuser/(?P<id>[0-9]+)/$',UsersViews.adminstopuser,name='admin_stop_user'),
    # 跟改步骤1
    url(r'^user/edituser/(?P<id>[0-9]+)/$',UsersViews.adminedituser,name='admin_edit_user'),
    # 跟改步骤2
    url(r'^updateuser/$',UsersViews.adminupdateuser,name='admin_update_user'),

    # 商品的分类
    # 商品分类添加页面
    url(r'^types/addtypes/$', TypeViews.adminaddtypes, name='admin_add_types'),
    # 插入表单提交的数据
    url(r'^types/inserttypes/$', TypeViews.admininserttypes, name='admin_insert_types'),
    # 分类列表
    url(r'^types/typeslist/$', TypeViews.admintypeslist, name='admin_list_types'),
    # 删除类别
    url(r'^types/typesdelete/(?P<id>[0-9]+)/$', TypeViews.admintypesdelete, name='admin_delete_types'),
    # 跟改类别
    url(r'^types/typesedit/$', TypeViews.admintypesedit, name='ajax_post'),



    # 商品
    # 添加
    url(r'^goods/addgoods/$', GoodsViews.adminaddgoods, name='admin_add_goods'),
    url(r'^goods/insertgoods/$', GoodsViews.admininsertgoods, name='admin_insert_goods'),
    # 商品列表的显示
    url(r'^goods/listgoods/$', GoodsViews.adminlistgoods, name='admin_list_goods'),
    # ajax 删除
    url(r'^goods/deletegoods/$', GoodsViews.admindeletegoods, name='admin_delete_goods'),
    # 返回form表单的方式重新编辑
    url(r'^goods/deitgoods/(?P<id>[0-9]+)/$', GoodsViews.admindeitgoods, name='admin_edit_goods'),
    url(r'^goods/updategoods/$', GoodsViews.adminupdategoods, name='admin_update_goods'),

    # 订单管理
    # 返回订单的列表
    url('^order/orderslist/$',OrderViews.OrderList,name='order_list'),
    # 删除订单
    url('^order/orderdel/$',OrderViews.OrderDel,name="order_del"),


    # auth 权限管理
    # auth   user的管理
    # 增加管理员用户
    url('^auth/user/adduser/$',AuthViews.AuthAddUser,name='auth_add_user'),
    # 管理员用户列表
    url('^auth/user/listuser/$',AuthViews.AuthListUser,name='auth_list_user'),
    # 管理员的删除
    url('^auth/user/deluser/$',AuthViews.AuthDelUser,name='auth_del_user'),


    # 用户组的管理
    # 用户组的添加
    url('^auth/group/addgroup/$',AuthViews.AuthAddGroup,name='auth_add_group'),
    # 用户组的列表
    url('^auth/group/listgroup/$',AuthViews.AuthListGroup,name='auth_list_group'),
    # 用户组的修改
    url('^auth/group/editgroup/$',AuthViews.AuthEditGroup,name='auth_edit_group'),



]