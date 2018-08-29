# -*- coding: utf-8 -*-

from django.http import HttpResponse
from TestModel.models import Student
from django.shortcuts import render_to_response, render


def add(request):
    name = request.POST['name']
    stu1 = Student(name=name)
    stu1.save()

    return render(request, 'index.html', {'info_add': '学生添加成功！'})

    # return HttpResponse("<p>学生添加成功！</p>")


def show(request):
    response = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Student.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Student.objects.filter(id=1)

    # 获取单个对象
    response3 = Student.objects.get(id=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    Student.objects.order_by('name')[0:2]

    # 数据排序
    print Student.objects.order_by("id")

    # 上面的方法可以连锁使用
    print Student.objects.filter(name="WangYu").order_by("id")

    for stu in list:
        response = response + stu.name + '\n'

    # return HttpResponse("<p>" + response + "</p>")

    return render(request, 'index.html', {'info': response})


def update(request):
    stu1 = Student.objects.get(id=1)
    stu1.name = '小明'
    stu1.save()

    # 另外一种方式
    Student.objects.filter(name="WangYu").update(name='小刚')

    # 修改所有的列
    # Student.objects.all().update(name='DQ')
    return HttpResponse("<p>修改成功</p>")


def delete(request):
    stu1 = Student.objects.get(id=1)
    stu1.delete()

    # 另外一种方式
    Student.objects.filter(name="WangYu").delete()

    # 修改所有的列
    # Student.objects.all().delete()
    return HttpResponse("<p>删除成功</p>")


def index(request):
    return render_to_response('index.html')
