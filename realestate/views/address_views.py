from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import json

from ..models import *


def address(request):
    cur_location = request.POST.get('location', '')
    jibun_bonbun = request.POST.get('jibun_bonbun', '')

    address_list = Address.objects.filter(lawd_cd=cur_location).order_by('jibun_bonbun', 'jibun_bubun')
    location_code = LocationCode.objects.order_by('location')

    context = {
        'list': address_list,
        'location_code_list': location_code,
        'jibun_bonbun': jibun_bonbun,
        'cur_location': cur_location,
    }
    return render(request, 'realestate/address.html', context)

def address_load(request):

    context = { }
    return render(request, 'realestate/address_load.html', context)

def address_upload(request):
    result = 'Fail'
    count = 0
    line_num = 0
    errors = []
    try:
        file_data = request.FILES.get('address_file')
        lines = file_data.read().decode('utf-8').split('\n')
        for line in lines:
            line_num += 1

            if line_num == 1 or len(line) == 0:
                continue

            tokens = line.split('|')
            if len(tokens) < 26:
                errors.append(line_num)
                continue

            # 우편번호|시도|시도영문|시군구|시군구영문|읍면|읍면영문|도로명코드|도로명|도로명영문|지하여부|건물번호본번|건물번호부번|건물관리번호|다량배달처명|시군구용건물명|법정동코드|법정동명|리명|행정동명|산여부|지번본번|읍면동일련번호|지번부번|구우편번호|우편번호일련번호
            address = Address()
            address.sido = tokens[1]
            address.sigungu = tokens[3]
            address.eupmyun = tokens[5]
            address.road_cd = tokens[7]
            address.road = tokens[8]
            address.road_bonbun = int(tokens[11])
            address.road_bubun = int(tokens[12])
            address.house_cd = tokens[13]
            address.lawd_cd = tokens[16]
            address.ri = tokens[18]
            address.is_san = int(tokens[20])
            address.jibun_bonbun = int(tokens[21])
            address.jibun_bubun = int(tokens[23])

            print(f'[{count}] {address.jibun_address()}')
            address.save()
            count += 1

        print(f'address count : {count}')
        result = 'Success'
    except Exception as e:
        print('address_upload() exception!', e)
        pass

    context = { 'result': result, 'count': count, 'errors': errors }
    return HttpResponse(json.dumps(context), content_type="application/json")
