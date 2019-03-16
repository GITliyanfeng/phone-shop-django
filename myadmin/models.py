from django.db import models

# Create your models here.
# 会员表
class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=80)
    phone = models.CharField(max_length=100)
    sex = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    email = models.CharField(max_length=100)
    pic = models.CharField(max_length=100,null=True,default='/static/pics/default.jpg')
    statu = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    # 自定义auth权限
    class Meta:
           permissions = (
               ('create_user','创建用户'),
               ('remove_user','删除用户'),
               ('remake_user','更改用户'),
               ('select_user','查询用户'),
           )


# 商品的分类表
class Types(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField()
    pid = models.IntegerField()
    path = models.CharField(max_length=10)
    addtime = models.DateTimeField(auto_now_add=True)
    topbar = models.IntegerField(default=0)

    class Meta:
           permissions = (
               ('create_type','创建商品分类'),
               ('remove_type','删除商品分类'),
               ('remake_type','更改商品分类'),
               ('select_type','查询商品分类'),
           )

# 商品表
class Goods(models.Model):
    tid = models.ForeignKey(to='Types',to_field='id')
    name = models.CharField(max_length=255)
    price = models.FloatField()
    pic = models.CharField(max_length=100)
    info = models.TextField()
    status = models.IntegerField(default=0)
    num = models.IntegerField()
    pointnum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
           permissions = (
               ('create_good','创建商品'),
               ('remove_good','删除商品'),
               ('remake_good','更改商品'),
               ('select_good','查询商品'),
           )

# 用户所对应的地址表
class Address(models.Model):
    uid = models.ForeignKey(to='Users', to_field='id')
    addressname = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    addressphone = models.CharField(max_length=11)
    isdefault = models.BooleanField(default=False)
    addressstatus = models.IntegerField(default=0)

# 订单模型和用户一对多
class Oredr(models.Model):
    '''
    字段：
        id  自增默认
        uid 和User表关联的外键
        addtime
        status 0 待付款 1 已付款待发货 2 已签收待评价 3 已取消
        address  外键和地址表id关联
        total  总计价格

    '''
    uid = models.ForeignKey(to='Users', to_field='id')
    addtime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    address = models.ForeignKey(to='Address',to_field='id')
    total = models.FloatField()

    class Meta:
           permissions = (
               ('create_order','创建订单'),
               ('remove_order','删除订单'),
               ('remake_order','更改订单'),
               ('select_order','查询订单'),
           )

# 订单详情
class OrderInfo(models.Model):
    '''
    字段：
        id  默认
        oid  和订单一对多关系
        goodname 名字
        goodprice  购买单价
        goodnum  购买数量
        goodsubtotal  单种商品的小计
        goodid   所对应的商品--在goods表中的id号码
    '''
    oid = models.ForeignKey(to='Oredr',to_field='id')
    goodname = models.CharField(max_length=30)
    goodprice = models.FloatField()
    goodpic = models.CharField(max_length=100)
    goodnum = models.IntegerField()
    goodid = models.IntegerField()
    goodsubtotal = models.FloatField()


