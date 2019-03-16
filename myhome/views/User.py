from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from myadmin.models import Users, Types, Goods, Address, Oredr, OrderInfo


# Create your views here.
# 返回列表页面
def UserList(request, tid):
    # 获取当前对象
    ob = Types.objects.get(id=tid)

    # 判断当前对象的等级
    if ob.level == 1:
        data = ob
        # 如果对象的等级是1级别，那么 {name:{一级},items:[{二级}，{列表}],goodsliset:[{商品},{}列表,{}]}
        data.items = Types.objects.filter(pid=ob.id)
        goodsindex = []
        for i in data.items:
            goodsindex.append(i.id)
        data.goodslist = Goods.objects.filter(tid__in=goodsindex)
        print(data)
    else:
        # 如果对象的等级是2级，那么，查父级
        data = Types.objects.get(id=ob.pid)
        # ，查这个父级了类别的所有子类<也就是当前子类的兄弟类>
        data.items = Types.objects.filter(pid=data.id)
        # 查 当前子类下的所有商品
        data.goodslist = Goods.objects.filter(tid=ob.id)
    # 分配数据
    context = {'data': data, 'ob': ob}
    # 解析模板
    # 解析模板
    return render(request, 'user/list.html', context)


# 返回详情页面
def UserInfo(request, gid):
    # 通过传送过来的商品id获取商品的详细信息
    data = Goods.objects.get(id=gid)
    # 分配数据
    context = {'data': data}
    # 解析模板
    return render(request, 'user/info.html', context)


# 注册页面 + 注册
def UserRegiser(request):
    if request.method == 'POST':
        # 执行正常注册
        try:
            data = request.POST.dict()
            if data['phonecode'] == request.session['msgcode']['code'] and data['phone'] == request.session['msgcode'][
                'phone']:
                # 删除验证信息
                data.pop('csrfmiddlewaretoken')
                data.pop('phonecode')
                # 加密
                data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
                # 将数据写入到数据库
                Users.objects.create(**data)
                return HttpResponse('<script>alert("注册成功");location.href="' + reverse("user_login") + '"</script>')
            else:
                return HttpResponse('<script>alert("短信验证码错误");location.href="' + reverse("user_login") + '"</script>')
        except:
            return HttpResponse('<script>alert("注册失败");location.href="' + reverse("user_regiser") + '"</script>')
    else:
        return render(request, 'user/register.html')


# 登录页面
def UserLogin(request):
    if request.method == "POST":
        nextpath = request.GET.dict().get('lastpath', None)
        if not nextpath:
            nextpath = reverse('home_index')
        print(nextpath)
        try:
            # 获取表单数据，执行登录操作
            data = request.POST.dict()
            # print(data)
            code = request.session.get('verifycode', default=None)
            # 验证用户
            ob = Users.objects.get(phone=data['phone'])
            if ob.statu == 1 or ob.statu == 2:
                return HttpResponse(
                    '<script>alert("账号异常");location.href="' + reverse(
                        "user_login") + '?lastpath=' + nextpath + '"</script>')

            if check_password(data['password'], ob.password):
                if data['verifycode'].upper() == code.upper():
                    request.session['VipUser'] = {'username': ob.username, 'id': ob.id, 'phone': ob.phone}
                    return HttpResponse('<script>alert("登录成功");location.href="' + nextpath + '"</script>')
                else:
                    return HttpResponse(
                        '<script>alert("验证码错误");location.href="' + reverse(
                            "user_login") + '?lastpath=' + nextpath + '"</script>')

            else:
                return HttpResponse(
                    '<script>alert("手机号或者密码错误");location.href="' + reverse(
                        "user_login") + '?lastpath=' + nextpath + '"</script>')
        except:
            return HttpResponse(
                '<script>alert("手机号或者密码错误");location.href="' + reverse(
                    "user_login") + '?lastpath=' + nextpath + '"</script>')
    else:
        return render(request, 'user/login.html')


# 图片验证码
def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 手机验证码
def phonecode(request):
    # 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    # 账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    # 注意事项：
    # （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    # （2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    # （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

    # import urllib2
    import urllib
    import json
    import random
    # 用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account = "C26351411"
    # 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "ae48809d5152bcf958356fcf70666491"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000, 99999))
    # 把验证码存入session
    request.session['msgcode'] = {'phone': mobile, 'code': code}
    text = "您的验证码是：" + code + "。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'}
    req = urllib.request.urlopen(
        url='http://106.ihuyi.com/webservice/sms.php?method=Submit',
        data=urllib.parse.urlencode(data).encode('utf-8')
    )
    content = req.read()
    res = json.loads(content.decode('utf-8'))
    print(res)
    return HttpResponse(res)


# 退出登录
def UserLogOut(requset):
    del requset.session['VipUser']
    return HttpResponse('<script>alert("退出成功");location.href="' + reverse("home_index") + '"</script>')


# 返回购物车页面
def UserCar(request):
    # 这里不作数据返回，直接使用session储存的数据
    return render(request, 'user/car.html')


# 添加购物车
def AddGood(request):
    try:
        gid = request.GET['gid']
        num = int(request.GET['num'])
        print(gid, '++++++++', num)
        # 获取商品的信息
        ob = Goods.objects.get(id=gid)
        goodinfo = {'name': ob.name, 'pic': ob.pic, 'price': ob.price, 'gid': ob.id, 'num': num}
        # 获取或者初始化session
        data = request.session.get('Cart', {})
        if gid in data:
            if data[gid]['num'] <= 5:
                data[gid]['num'] += num
            else:
                return JsonResponse({'error': 2, 'msg': '加入购物车失败，限购5件'})
        else:
            data[gid] = goodinfo
        # 写入session信息
        request.session['Cart'] = data
        msg = request.session.get('Cart')
        print(msg)
        return JsonResponse({'error': 0, 'msg': '加入购物车成功'})
    except:
        return JsonResponse({'error': 1, 'msg': '加入购物车失败'})


# 修改购物车而
def GoodEdit(request):
    try:
        gid = request.GET['gid']
        num = request.GET['num']
        # print(gid,type(gid))
        # print(num,type(num))
        # 修改session
        data = request.session.get('Cart')
        if data[gid]['num'] <= 5:
            data[gid]['num'] = int(num)
        else:
            return HttpResponse('<script>alert("每人限购5件");location.href="' + reverse('user_car') + '"</script>')
        request.session['Cart'] = data
        return HttpResponse('<script>location.href="' + reverse('user_car') + '"</script>')
    except:
        return HttpResponse('<script>alert("添加失败");location.href="' + reverse('user_car') + '"</script>')


# 删除购物车中的某个商品
def GoodDel(request):
    gid = request.GET['gid']
    # 获取session，将想要删除的部分del掉
    data = request.session.get('Cart', {})
    del data[gid]
    # 将修改后的session数据重新写会session
    request.session['Cart'] = data
    # 跳转
    return HttpResponse('<script>location.href="' + reverse('user_car') + '"</script>')


# 清空购物车
def GoodFlushi(request):
    try:
        del request.session['Cart']
        return HttpResponse('<script>alert("购物车已经清空");location.href="' + reverse('user_car') + '"</script>')
    except:
        return HttpResponse('<script>alert("购物车已是清空状态");location.href="' + reverse('user_car') + '"</script>')


# 确认订单
def OrderMake(request):
    '''
    确认订单的页面，需要的数据是？
        1. 地址
        2.所购买的商品信息
            1.商品id
            2.商品名
            3.商品单价---此时数据库中的单价
            4.商品小计
            5.商品数量
            6.商品图片

    :param request:
    :return:
    '''
    # 用户
    uid = request.session['VipUser']['id']
    # 数据1---地址
    address = Address.objects.filter(uid=uid)
    # 数据2---商品
    gids = request.GET.dict()['gids']
    strgids = gids
    cart = request.session['Cart']
    gids = gids.split(',')
    data = []
    for x in gids:
        data.append({'name': cart[str(x)]['name'], 'pic': cart[str(x)]['pic'], 'price': Goods.objects.get(id=x).price,
                     'num': cart[str(x)]['num'], 'gid': x})
    context = {'address': address, 'data': data, 'strgids': strgids}
    return render(request, 'user/createorder.html', context)


# 生成订单信息
def OrderCreate(request):
    '''
    生成订单需要什么数据？
        1.谁的订单   uid
              info表   2.订单中有什么？
                    1.商品 gid
                    2.商品名字
                    3.商品单价
                    4.商品数量
                    5.商品小计
        3.订单的总计价格 初始设置为0，然后在根据info表的计算结果更改
        4.订单要发送给谁？
            uid--->aid
    :param request:
    :return:
    '''
    data_order = {}
    # 数据3初始化总价是0
    data_order['total'] = 0
    # 数据4地址aid
    data_order['address'] = Address.objects.get(id=request.POST.dict()['aid'])
    # 数据1 是谁
    uid = request.session['VipUser']['id']
    data_order['uid'] = Users.objects.get(id=uid)
    # 生成订单记录
    order = Oredr.objects.create(**data_order)
    # 数据2买了什么？
    strgids = request.POST.dict()['gids']
    res = request.session['Cart']
    print(res)
    gids = strgids.split(',')
    for i in gids:
        # 初始化一个info
        info = OrderInfo()
        # oid
        info.oid = order
        # name
        info.goodname = res[str(i)]['name']
        # num
        info.goodnum = res[str(i)]['num']
        # price
        info.goodprice = Goods.objects.get(id=i).price
        # 所对应的商品的id号码
        info.goodid = int(i)
        # 商品的图片
        info.goodpic = Goods.objects.get(id=i).pic
        # subtotal
        info.goodsubtotal = int(info.goodnum) * float(info.goodprice)
        # 将总价加上一次小计
        data_order['total'] += info.goodsubtotal
        # 减库存
        good = Goods.objects.get(id=i)
        good.num -= 1
        # 保存对Goods表减去库存的修改
        good.save()
        # 保存对orderinfo表的修改
        info.save()
        # 删除购物车中的已购买的商品【session】
        bycar = request.session['Cart']
        bycar.pop(str(i))
        request.session['Cart'] = bycar
    order.total = data_order['total']
    # 保存对订单的修改
    order.save()
    # 跳转到付款界面----这个过程已经生成了订单,将当前生成的订单以字符串的拼接的方式传递出去
    return HttpResponse(
        '<script>location.href="' + reverse('order_pay_for') + '?order_number=' + str(order.id) + '"</script>')


# 跳转到付款的界面
def OrderPayFor(request):
    uid = request.GET.get('order_number')
    print(uid)
    order = Oredr.objects.get(id=uid)
    data = {}
    data.update(
        {'name': order.address.addressname, 'total': order.total, 'id': order.id, 'addr': order.address.address})
    context = {'data': data}
    return render(request, 'user/payfor.html', context)


# 更改当前订单的状态为1，已付款代发货
def OrderPayFored(request):
    id = request.GET.get('id', None)
    ob = Oredr.objects.get(id=id)
    ob.status = 1
    ob.save()
    # 跳转
    print('xxxxxx')
    return JsonResponse({'msg': '付款成功'})


# 点击付款，跳转到付款成功的页面
def OrderPayForSuccess(request):
    #

    return render(request, 'user/payforsuccess.html')


# 跳转到我的订单列表界面
def MyOrderList(request):
    # 查询当前用户下的所有订单
    uid = request.session['VipUser']['id']
    # 通过用户去查找用户下的所有订单
    if request.GET.get('type', None):
        mytype = request.GET.get('type', None)
        keyword = request.GET.get('keyword', None)
        info = {mytype: keyword}
        order_data = Oredr.objects.filter(uid=uid).filter(**info)
    else:
        order_data = Oredr.objects.filter(uid=uid)
    # 分配数据
    context = {'data': order_data}
    return render(request, 'user/myorderlist.html', context)


# 添加地址
def AddAdderss(request):
    lastspace = request.GET.get('space', None)
    if not lastspace:
        try:
            # 从网页获取地址数据
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            # 在这里存在一个问题，默认地址，一个用户只能有一个，通过uid查询当前id下有没有默认地址，如果没有，直接添加
            # ，否则，将其他的地址改为非默认，当前添加的地址，改为默认
            gids = data.pop('gids')
            if data['isdefault'] == '1':
                try:
                    default_address = Users.objects.get(id=data['uid']).address_set.get(isdefault=True)
                except:
                    default_address = None
                if default_address:
                    default_address.isdefault = 0
                    default_address.save()
            # 获取外键对象
            user = Users.objects.get(id=data['uid'])
            data['uid'] = user
            # 添加数据
            Address.objects.create(**data)
            return HttpResponse(
                '<script>alert("增加地址成功");location.href="' + reverse('order_make') + '?gids=' + gids + '"</script>')
        except:
            return HttpResponse(
                '<script>alert("增加地址失败");location.href="' + reverse('order_make') + '?gids=' + gids + '"</script>')
    else:
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            if data['isdefault'] == '1':
                try:
                    default_address = Users.objects.get(id=data['uid']).address_set.get(isdefault=True)
                except:
                    default_address = None
                if default_address:
                    default_address.isdefault = 0
                    default_address.save()
                # 获取外键对象
            user = Users.objects.get(id=data['uid'])
            data['uid'] = user
            # 添加数据
            Address.objects.create(**data)
            return HttpResponse('<script>alert("增加地址成功");location.href="' + lastspace + '"</script>')
        except:
            return HttpResponse('<script>alert("增加地址失败");location.href="' + lastspace + '"</script>')


# 地址管理器
def AdderssManage(request):
    uid = request.session['VipUser']['id']
    address_data = Address.objects.filter(uid=uid)
    context = {'data': address_data}
    return render(request, 'user/addressmanage.html', context)


# 删除地址
def AdderssManageDelete(request):
    '''
    删除地址的条件：
        1.知道地址的id
        2.订单中没有人在用这个地址---也就说使用这条地址的订单已经被删除，
        3.只做逻辑删除，不做物理删除
    :param request:
    :return:
    '''
    try:
        id = request.GET.get('aid', None)
        # print(id)
        ob = Address.objects.get(id=id)
        # print(ob)
        res = ob.oredr_set.exclude(status=3)
        # print(res)
        if not res:
            # print('地址不再被占用')
            ob.addressstatus = 1
            ob.isdefault = False
            ob.save()
            return HttpResponse('<script>alert("删除地址成功");location.href="' + reverse('address_manage') + '"</script>')
        else:
            return HttpResponse(
                '<script>alert("地址被占用，删除地址失败");location.href="' + reverse('address_manage') + '"</script>')
    except:
        return HttpResponse('<script>alert("发生错误，删除地址失败");location.href="' + reverse('address_manage') + '"</script>')


# 跟改地址
def AdderssManageUpdate(request):
    try:
        id = request.GET.get('aid')
        ob = Address.objects.get(id=id)
        # 判断这个地址是否正在被使用
        res = ob.oredr_set.exclude(status=3)
        if not res:
            data = request.POST.dict()
            ob.addressname = data['addressname']
            ob.addressphone = data['addressphone']
            ob.address = data['address']
            # 更改默认是个问题，得确定默认地址是否已经存在
            uid = request.session['VipUser']['id']
            try:
                defaultaddr = Address.objects.filter(uid=uid).get(isdefault=True)
                info = defaultaddr.isdefault
            except:
                info = None
            if not info:
                ob.isdefault = data.get('isdefault', False)
            else:
                # 先将已存在的默认地址改为False
                defaultaddr.isdefault = False
                defaultaddr.save()
                ob.isdefault = data.get('isdefault', False)
            ob.save()
            return HttpResponse('<script>alert("地址修改成功");location.href="' + reverse('address_manage') + '"</script>')
        else:
            return HttpResponse(
                '<script>alert("地址被占用，无法修改");location.href="' + reverse('address_manage') + '"</script>')
    except:
        return HttpResponse('<script>alert("发生错误，修改地址失败");location.href="' + reverse('address_manage') + '"</script>')


# 解析个人中心
def MyCenter(request):
    id = request.session['VipUser']['id']
    user = Users.objects.get(id=id)
    order_pay = Oredr.objects.filter(uid=id).filter(status=1)
    order_unpay = Oredr.objects.filter(uid=id).filter(status=0)
    context = {'data': user, 'order_pay': order_pay, 'order_unpay': order_unpay}
    return render(request, 'user/owencenter.html', context)


# 初始化密码
def Init(request):
    obs = Users.objects.all()
    for i in obs:
        i.password = make_password('000000', None, 'pbkdf2_sha256')
        i.save()
    return HttpResponse('初始化所有密码')


# 模拟缓存测试需要导入的包
import datetime
from django.views.decorators.cache import cache_page
from django.core.cache import cache


# 缓存测试1----10秒内缓存整个视图函数获取的数据
@cache_page(10)
def cache1(request):
    t = datetime.datetime.now()
    return HttpResponse(t)


# 缓存测试2
def cache2(request):
    # 判断是否已经有缓存
    a = cache.get('time', None)
    if a:
        print('已经有缓存')
        print('time is :', a)
    else:
        print('没有缓存')
        a = datetime.datetime.now()
        cache.set('time', a, 5)
        print('time is :', a)
    return HttpResponse(a)
