# -*- coding: utf-8 -*-
# @Time    : 18-9-12 下午1:47
# @Author  : Gold_py
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from .views import IndexViews,User


urlpatterns = [
    # 跳转到商城的首页面
    url(r'^$', IndexViews.homeindex,name='home_index' ),
    # 商城的列表页面
    url(r'^list/(?P<tid>[0-9]+)/$',User.UserList,name='user_list'),
    # 商城商品的详情页面
    url(r'^info/(?P<gid>[0-9]+)/$',User.UserInfo,name='user_info'),
    # 商城的注册界面
    url(r'^register/$',User.UserRegiser,name='user_regiser'),
    # 商城的登录界面
    url(r'^login/$',User.UserLogin,name='user_login'),
    # 验证码的生成位置
    url(r'^passcode/$',User.verifycode,name='user_pass_code'),
    # 获取手机验证码
    url(r'^phonecode/$',User.phonecode,name='user_phone_code'),
    # 退出都登录
    url(r'^logout/$',User.UserLogOut,name='user_log_out'),
    # 购物车
    url(r'^bycar/$',User.UserCar,name='user_car'),
    # 加入购物车
    url(r'^bycar/addgood/$',User.AddGood,name='add_good'),
    # 跟改购物车
    url(r'^bycar/edit_good/$',User.GoodEdit,name='good_edit'),
    # 删除购物车中的某个商品
    url(r'^bycar/del_good/$',User.GoodDel,name='good_del'),
    # 清除购物车
    url(r'^bycar/flush/$',User.GoodFlushi,name='good_flush'),



    # 以下的操作需要获取登录认证



    # 商城跳转到确认订单的页面
    url(r'^order/confirm/$',User.OrderMake,name='order_make'),
    # 生成订单
    url(r'^order/create/$',User.OrderCreate,name='order_create'),
    # 跳转到付款的界面
    url(r'^order/payfor/$',User.OrderPayFor,name='order_pay_for'),
    # 订单状态改变为1，已付款
    url(r'^order/payfored/$',User.OrderPayFored,name='order_pay_fored'),
    # 跳转到付款成功界面
    url(r'^order/payforsuccess/$',User.OrderPayForSuccess,name='order_pay_for_suscess'),
    # 跳转到我的订单界面
    url(r'^my/order/orderlist/$',User.MyOrderList,name='my_order_list'),


    # 添加地址
    url(r'^user/addaddress/$',User.AddAdderss,name='add_address'),
    # 地址管理器
    url(r'address/manage/$',User.AdderssManage,name='address_manage'),
    # 删除地址
    url(r'address/manage/delete/$',User.AdderssManageDelete,name='address_manage_delete'),
    # 跟改地址
    url(r'address/manage/update/$',User.AdderssManageUpdate,name='address_manage_update'),


    # 个人中心
    url('^user/mycenter/$',User.MyCenter,name='my_center'),
    # 更改个人信息
    url('^user/mycenter/$',User.MyCenter,name='my_center'),


    # 初始化密码
    url('^init/$',User.Init,name='init'),




    # 缓存测试
    url('^cache1/$',User.cache1,name='cache1'),
    url('^cache2/$',User.cache2,name='cache2'),





]