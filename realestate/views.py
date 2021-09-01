from django.http.response import HttpResponse
from django.shortcuts import render, redirect

import time
import json

from .models import MyLandItem
from .ItemInfo import ItemInfo
import naver.land as nl


json_save_path = './realestate/json'

# Create your views here.
def index(request):
    my_list = MyLandItem.objects.filter(is_favorite=True)
    result_list = []

    for item in my_list:
        land_item = nl.LandItem.createFromJson(json_save_path, item.article_no, item.article_confirm_ymd)

        item_info = ItemInfo()
        item_info.id = item.id
        item_info.article_no = item.article_no
        item_info.article_confirm_ymd = land_item.confirm_day
        item_info.price = land_item.price
        if land_item.area == 0:
            item_info.price_per_area = 0
        else:
            item_info.price_per_area = int(land_item.price / land_item.area * 3.3)
        item_info.area = land_item.area
        item_info.building_area = land_item.building_area
        item_info.total_floor_area = land_item.total_floor_area
        item_info.address = land_item.address
        item_info.memo = item.memo
        result_list.append(item_info)

    result_list.sort(key=lambda item: (item.address, item.article_no))
    context = { 'list': result_list }
    return render(request, 'realestate/item_list.html', context)

def detail(request, listitem_id):
    item = MyLandItem.objects.get(id=listitem_id)
    json_path = f'{json_save_path}/{nl.LandItem.getJsonFileNameS(item.article_no, item.article_confirm_ymd)}'
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_object = json.load(json_file)
    context = { 'item': item, 'json': json_object }
    return render(request, 'realestate/item_detail.html', context)

def item_modify(request, listitem_id):
    item = MyLandItem.objects.get(id=listitem_id)
    item.memo = request.POST.get('memo')
    item.save()
    return redirect('realestate:index')

def naver(request):
    result_list = []
    is_more_data = False
    cur_location = request.POST.get('location')
    building_types = request.POST.getlist('building_type')
    is_building_type_ddonly = False
    if request.POST.get('building_type_ddonly') is not None:
        is_building_type_ddonly = True
    old_build_years = request.POST.get('old_build_years')
    if old_build_years is None:
        old_build_years = ''
    recently_build_years = request.POST.get('recently_build_years')
    if recently_build_years is None:
        recently_build_years = ''
    name_except_filter = request.POST.get('name_except_filter')
    if name_except_filter is None:
        name_except_filter = ''
    else:
        name_except_filter = name_except_filter.strip()
    page = request.POST.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    article_no = request.POST.get('article_no')

    if article_no is not None and 0 < len(article_no):
        land_item = nl.LandItem()
        land_item.parseFromID(article_no)
        land_item.calcBuildYears()
        result_list.append(land_item)
    elif cur_location is not None:
        list_crawler = nl.LandListCrawler()
        list_crawler.setBuildingType(building_types)
        list_crawler.setWithinYears(old_build_years, recently_build_years)
        if 0 < len(name_except_filter):
            list_crawler.setNameExceptFilter(name_except_filter.split(','))
        is_more_data, land_list = list_crawler.parse(cur_location, page)

        for item in land_list:
            my_item_list = MyLandItem.objects.filter(article_no=item.articleNo)
            my_item = None
            if len(my_item_list) == 0:
                my_item = MyLandItem.objects.create(
                                                    article_no=item.articleNo,
                                                    article_confirm_ymd=item.articleConfirmYmd)
            else:
                my_item = my_item_list.first()
                if my_item.article_confirm_ymd != item.articleConfirmYmd:
                    my_item.article_confirm_ymd = item.articleConfirmYmd
                    my_item.is_new = True
                    my_item.save()

            # 단독only 조건일 경우 다가구 제외        
            if is_building_type_ddonly and my_item.is_multi_family is not None and my_item.is_multi_family:
                continue

            land_item = nl.LandItem()
            json_file_path = f'{json_save_path}/{nl.LandItem.getJsonFileNameS(my_item.article_no,my_item.article_confirm_ymd)}'
            # 이미 저장된 아이템일 경우 json 파일 읽기
            if land_item.loadJson(json_file_path) == False:
                # 신규 또는 확인날짜가 바뀌었을 경우 상세정보 json 파일 다운로드
                time.sleep(0.3)
                land_item.parseFromID(my_item.article_no)
                land_item.saveJson(json_save_path)

            land_item.is_new = my_item.is_new
            land_item.is_favorite = my_item.is_favorite
            land_item.is_multi_family = my_item.is_multi_family
            land_item.calcBuildYears()
            result_list.append(land_item)

    result_list.sort(key=lambda item: item.address)
    context = {
        'list': result_list,
        'page': page,
        'is_more_data': is_more_data,
        'location_code_list': nl.location_code,
        'building_type_list': nl.building_type,
        'cur_location': cur_location,
        'building_types': building_types,
        'is_building_type_ddonly': is_building_type_ddonly,
        'old_build_years': old_build_years,
        'recently_build_years': recently_build_years,
        'name_except_filter': name_except_filter,
    }
    return render(request, 'realestate/naver.html', context)

def check(request):
    result = 'Fail'
    try:
        article_no = request.POST.get('article_no')
        my_item = MyLandItem.objects.get(article_no=article_no)
        my_item.is_new = False
        my_item.save()
        result = 'Success'
    except:
        pass

    context = {
        'article_no': article_no,
        'result': result,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def favorite(request):
    result = 'Fail'
    try:
        article_no = request.POST.get('article_no')
        my_item = MyLandItem.objects.get(article_no=article_no)
        my_item.is_new = False
        my_item.is_favorite = True
        my_item.save()
        result = 'Success'
    except:
        pass

    context = {
        'article_no': article_no,
        'result': result,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")

def multi(request):
    result = 'Fail'
    try:
        article_no = request.POST.get('article_no')
        is_multi_family = request.POST.get('is_multi_family')
        my_item = MyLandItem.objects.get(article_no=article_no)
        if is_multi_family == 'True':
            my_item.is_multi_family = True
        else:
            my_item.is_multi_family = False
        my_item.is_new = False
        my_item.save()
        result = 'Success'
    except:
        pass

    context = {
        'article_no': article_no,
        'result': result,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")
