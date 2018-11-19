# -*- coding: utf-8 -*-

import random, json, copy
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


def find_optimal(request):
    l = []
    for i in range(1000):
        p = random.randint(1, 9)
        if p not in l:
            l.append(p)
            if len(l) == 8:
                break
    if len(l) % 2 != 0:
        for i in range(1000):
            p = random.randint(1, 9)
            if p not in l:
                l.append(p)
                break

    context = {'first': l[0],
               'last': l[-1],
               'list': l,
               'AI_sum': 0,
               'Player_sum': 0,
               'AI_picks': [],
               'Player_picks': []
               }
    return render(request, 'find_optimal.html', context)


def calculate(request):
    l = eval(request.POST['list'])

    Player_sum = eval(request.POST['Player_sum'])
    AI_sum = eval(request.POST['AI_sum'])
    Player_picks = eval(request.POST['Player_picks'])
    AI_picks = eval(request.POST['AI_picks'])

    input_choose = request.POST['index']

    if input_choose != 'AI':
        index = 0 if input_choose == 'First' else -1
        Player_picks.append(l[index])
        Player_sum += l[index]
        del (l[index])
    if l:
        AI_pick = xunhuan(l)
        l.remove(AI_pick)
        AI_sum += AI_pick
        AI_picks.append(AI_pick)

    if not l:
        context = {'first': 0,
                   'last': 0,
                   'list': l,
                   'AI_sum': AI_sum,
                   'Player_sum': Player_sum,
                   'AI_picks': AI_picks,
                   'Player_picks': Player_picks
                   }
    else:
        context = {'first': l[0],
                   'last': l[-1],
                   'list': l,
                   'AI_sum': AI_sum,
                   'Player_sum': Player_sum,
                   'AI_picks': AI_picks,
                   'Player_picks': Player_picks
                   }
    return render(request, 'find_optimal.html', context)


def xunhuan(l):
    if len(l) == 1:
        return l[0]
    q = [0, -1]
    for i in range(len(l) - 1):
        new_q = []
        for x in q:
            for y in [0, -1]:
                zz = []
                zz.append(x)
                zz.append(y)
                new_q.append(zz)
        q = new_q

    s1_max_sum = 0
    s1_max_pick = []
    for m in q:
        s1_pick = []
        s2_pick = []
        seq = flat(m)
        new_l = copy.deepcopy(l)
        for i, index in enumerate(seq):
            if not new_l:
                break
            if i % 2 == 0:
                s1_pick.append(new_l[index])
                del (new_l[index])
            else:
                s2_pick.append(new_l[index])
                del (new_l[index])

        if sum(s1_pick) > s1_max_sum:
            s1_max_sum = sum(s1_pick)
            s1_max_pick = s1_pick

    print s1_max_pick, s1_max_sum
    return s1_max_pick[0]


def flat(nums):
    res = []
    for i in nums:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res
