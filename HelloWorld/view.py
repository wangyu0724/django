# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def study(request):
    context = {
        'yes': '哈哈哈，我想学Python',
        'no': '嘿嘿嘿，我不想学了',
        'subject': {'python': ['a', 'b'],
                    'java': ['c', 'd'],
                    'react': ['e', 'f'],
                    'nodejs': ['g', 'h']},
        'flag': 'true1'

    }
    return render(request, 'hello.html', context)
