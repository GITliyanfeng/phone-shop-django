from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required

from ..models import Types
from django.db.models import Q


# Create your views here.
@permission_required('myadmin.create_type',raise_exception=True)
def adminaddtypes(request):
    # 返回一个form表单来执行添加
    # 返回下拉框中可选择的父级类别
    # 获取数据库中的数据
    data = SelectAndOrder()
    # 分配数据
    context = {'data': data}
    # 解析模板
    return render(request, 'admin/types/typeadd.html', context)

@permission_required('myadmin.create_type',raise_exception=True)
# 插入表单提交的分类数据
def admininserttypes(request):
    # try:
    # 获取数据
    data = request.POST.dict()
    # 删除验证
    data.pop('csrfmiddlewaretoken')
    # 当前data只能提供pid和name两个数据  如何获得level以及path？
    # 如果pid = 0 那么他的等级就是1
    pid = int(data['pid'])
    if pid == 0:
        level = 1
        # 如果等级不是0，那么level就是父级的level+1
    else:
        level = Types.objects.get(id=pid).level + 1
    data['level'] = level
    data['pid'] = pid
    # 此时pid name level都有了，还差一个path，当level = 1 时候 path = 0,
    if data['level'] == 1:
        path = '0,'
    else:
        # 如果level不是1，那么他的path就是父级的path+pid+,字符串的拼接
        path = Types.objects.get(id=pid).path + str(pid) + ','
    data['path'] = path
    # 将组合完毕的数据添加到数据库
    Types.objects.create(**data)

    return HttpResponse('<script>alert("添加成功");location.href="' + reverse('admin_list_types') + '"</script>')


# 定义查询后排序函数
def SelectAndOrder():
    # select *,concat(path,id) as paths from myadmin_types order by paths:
    data = Types.objects.extra(select={'paths': 'concat(path,id)'}).order_by('paths')
    for i in data:
        if i.pid == 0:
            i.pname = '顶级分类'
        else:
            ob = Types.objects.get(id=i.pid)
            i.pname = ob.name
    # 返回查询到的数据
    return data


# 执行查询  排序 分页 的操作后  返回列表页面
@permission_required('myadmin.select_type',raise_exception=True)
def admintypeslist(request):
    # 排序后输出
    # data = Types.objects.all()
    data = SelectAndOrder()
    # 关键查询
    type = request.GET.get('type','name')
    keyword = request.GET.get('keyword', '')
    # 过滤查询--将排完序号的数据进行二次过滤
    info = {type + '__contains': keyword}
    data = data.filter(**info)
    # 分页管理
    # 实例化分页
    p = Paginator(data, 6)
    # 获取页面的页码
    page = request.GET.get('page', 1)
    # 获取组合页面数据
    typeslist = p.page(page)
    # 分配数据
    context = {'data': typeslist}
    # 解析模板
    # print(context)
    return render(request, "admin/types/typelist.html", context)


# 删除类别
@permission_required('myadmin.remove_type',raise_exception=True)
def admintypesdelete(request, id):
    try:
        # 获取对象
        ob = Types.objects.get(id=int(id))
        # 删除需要判断
        # 1 判断要删除的类下是否还有子类
        childrens = Types.objects.filter(pid=ob.id)
        res = {}
        if childrens:
            res['err_code'] = 1
            res['msg'] = '当前类别之下还存在子类别'
            return HttpResponse('<script>alert("无法删除' + res['msg'] + '");location.href="' + reverse('admin_list_types') + '"</script>')
        else:
            ob.delete()
            return HttpResponse('<script>alert("删除成功");location.href="' + reverse('admin_list_types') + '"</script>')
        # 2 判断要删除的类下是否还有商品
    except:
        return HttpResponse('<script>alert("删除失败");location.href="' + reverse('admin_list_types') + '"</script>')


# ajax 请求  修改类名
@permission_required('myadmin.remake_type',raise_exception=True)
def admintypesedit(request):
    res = {}
    try:
        # 获取传送过来的id
        id = request.GET.get('id')
        newname = request.GET.get('newname')
        # 获取数据库中的数据
        ob = Types.objects.get(id=int(id))
        # 更改数据
        ob.name = newname
        ob.save()
        res['err_code'] = 0
        res['msg'] = '修改成功'
        return JsonResponse(res)
    except:
        res['err_code'] = 1
        res['msg'] = '修改失败'
        return JsonResponse(res)

