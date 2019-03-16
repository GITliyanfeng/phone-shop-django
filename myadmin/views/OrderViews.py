from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from ..models import Oredr,OrderInfo,Goods,Address
from django.db.models import Q


# Create your views here.


def OrderList(request):
    # 查询所有的订单，然后显示出来,addtime排序
    orders_data = Oredr.objects.all().order_by('addtime')
    # 实例化分页
    p = Paginator(orders_data, 5)
    # 获取页面的页码
    page = request.GET.get('page', 1)
    # 获取组合页面数据
    typeslist = p.page(page)
    # 分配数据
    context = {'data': typeslist}

    return render(request, 'admin/order/orderlist.html',context)
# 删除定订单
def OrderDel(request):
    id = request.GET['id']
    ob = Oredr.objects.get(id=id)
    ob.delete()
    return HttpResponse('<script>alert("删除订单");location.href="'+reverse('order_list')+'"</script>')
