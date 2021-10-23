from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

import json

from ..util import *
from gov.nsdi.lawdcd import LawdCD


def jibun_list(request):
    category = request.POST.get('category', 'sido')
    lawd_cd = request.POST.get('lawd_cd', '')
    if category == 'sigungu':
        code = lawd_cd[0:2]
    elif category == 'eupmyundong':
        code = lawd_cd[0:5]
    elif category == 'ri':
        code = lawd_cd[0:8]
    else:
        code = ''
    list = LawdCD.search(code)
    result = 'Success'
    context = { 'result': result, 'list': list }
    return JsonResponse(context, encoder=MyJsonEncoder)
