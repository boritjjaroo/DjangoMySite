from django.http.response import HttpResponse
from django.shortcuts import render, redirect

import time
import json
import os

from .models import Realestate
from .models import MyLandItem
from .models import LocationCode
from .ItemInfo import ItemInfo
import naver.land as nl
import gov.molit as molit


json_save_path = './realestate/json'
land_image_path = './static/pic/realestate'
land_file_path = './static/file/realestate'

# Create your views here.
def index(request):
    my_list = MyLandItem.objects.filter(is_favorite=True)
    result_list = []

    for item in my_list:
        land_item = nl.LandItem.createFromJson(json_save_path, item.article_no, item.article_confirm_ymd)
        land_item.calcBuildYears()

        if item.initial_price is None:
            land_item.getPriceHistory()
            item.initial_price = land_item.initial_price
            item.save()

        item_info = ItemInfo()
        item_info.id = item.id
        item_info.parent_id = item.parent_id
        item_info.article_no = item.article_no
        item_info.article_confirm_ymd = land_item.confirm_day
        item_info.price = land_item.price
        item_info.initial_price = item.initial_price
        if land_item.area == 0:
            item_info.price_per_area = 0
        else:
            item_info.price_per_area = int(land_item.price / land_item.area * 3.3)
        item_info.area = land_item.area
        item_info.building_area = land_item.building_area
        item_info.total_floor_area = land_item.total_floor_area
        item_info.address = land_item.address
        item_info.build_years = land_item.build_years
        item_info.memo = item.memo
        item_info.count = 0
        if item.declared_value is not None:
            item_info.declared_value = item.declared_value
            item_info.declared_value_date = item.declared_value_date
        result_list.append(item_info)

    result_list.sort(key=lambda item: (item.address, item.article_no))

    # 같은 항목 개수 세기
    parent_item_info = ItemInfo()
    for item_info in result_list:
        if item_info.parent_id == 0:
            item_info.count = 1
            parent_item_info = item_info
        elif item_info.parent_id == parent_item_info.id:
            parent_item_info.count = parent_item_info.count + 1

    context = { 'list': result_list }
    return render(request, 'realestate/item_list.html', context)

def index2(request):
    result_list = []
    realestate_list = Realestate.objects.order_by('address_jibun')

    for item in realestate_list:
        my_list = MyLandItem.objects.filter(realestate_id=item.id).order_by('article_no')
        iteminfo = ItemInfo()
        iteminfo.realestate = item

        # 가격정보 null 일 경우 json 파싱해서 값 가져오기
        for myitem in my_list:
            if myitem.price is None or myitem.price == 0:
                land_item = nl.LandItem.createFromJson(json_save_path, myitem.article_no, myitem.article_confirm_ymd)
                myitem.price = land_item.price
                myitem.save()

        iteminfo.mylist = my_list
        result_list.append(iteminfo)

    context = { 'list': result_list }
    return render(request, 'realestate/item_list2.html', context)

def detail(request, listitem_id):
    item = MyLandItem.objects.get(id=listitem_id)
    json_path = f'{json_save_path}/{nl.LandItem.getJsonFileNameS(item.article_no, item.article_confirm_ymd)}'
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_object = json.load(json_file)

    # 이미지 목록 가져오기
    image_list = []
    image_dir = land_image_path + '/' + item.article_no
    if os.path.isdir(image_dir):
        image_list = os.listdir(image_dir)

    pretty_json = json.dumps(json_object, indent=4, ensure_ascii=False)
    context = { 'item': item, 'json': pretty_json, 'image_list': image_list }
    return render(request, 'realestate/item_detail.html', context)

def detail2(request, listitem_id):
    item = Realestate.objects.get(id=listitem_id)

    # 이미지 목록 가져오기
    image_list = []
    if item.file_prefix:
        image_dir = land_image_path + '/' + item.file_prefix + '/'
        if os.path.isdir(image_dir):
            image_list = os.listdir(image_dir)

    # 첨부파일 목록 가져오기
    file_list = []
    if item.file_prefix:
        file_dir = land_file_path + '/' + item.file_prefix + '/'
        if os.path.isdir(file_dir):
            file_list = os.listdir(file_dir)

    context = { 'item': item, 'image_list': image_list, 'file_list': file_list }
    return render(request, 'realestate/item_detail2.html', context)


def json_view(request, article_no):
    json_object = None
    json_path = f'{json_save_path}/'
    json_list = os.listdir(json_path)
    for json_file in json_list:
        if json_file.startswith(str(article_no)):
            file_path = f'{json_save_path}/{json_file}'
            with open(file_path, 'r', encoding='utf-8') as json_file:
                json_object = json.load(json_file)
            break
    pretty_json = json.dumps(json_object, indent=4, ensure_ascii=False)
    context = { 'json': pretty_json }
    return render(request, 'realestate/json_view.html', context)

def item_modify(request, listitem_id):
    item = MyLandItem.objects.get(id=listitem_id)
    item.parent_id = request.POST.get('parent_id')
    item.memo = request.POST.get('memo')
    item.save()
    return redirect('realestate:index')

def item_modify2(request, listitem_id):
    item = Realestate.objects.get(id=listitem_id)
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

            if my_item.initial_price is None:
                land_item.getPriceHistory()
                my_item.initial_price = land_item.initial_price
                my_item.save()
            else:
                land_item.initial_price = my_item.initial_price

            land_item.is_new = my_item.is_new
            land_item.is_favorite = my_item.is_favorite
            land_item.is_multi_family = my_item.is_multi_family
            land_item.calcBuildYears()
            result_list.append(land_item)

    result_list.sort(key=lambda item: item.address)

    location_code = LocationCode.objects.order_by('location')

    context = {
        'list': result_list,
        'page': page,
        'is_more_data': is_more_data,
        'location_code_list': location_code,
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


def price(request):
    price_list = []
    amount_average = 0
    amount_min = 9999999999
    amount_max = 0

    search_location = request.POST.get('search_location')
    search_category = request.POST.get('search_category')
    search_year = request.POST.get('search_year')
    filter_location = request.POST.get('filter_location')
    filter_address = request.POST.get('filter_address')
    filter_jimok = request.POST.get('filter_jimok')
    filter_usage = request.POST.get('filter_usage')
    filter_road = request.POST.get('filter_road')

    #print(filter_location)

    if search_location is not None:
        search_results = molit.get_real_sale_price(search_category, search_location, search_year)

        print(f'국토부 검색결과 {len(search_results)}개')
        #print(search_results)

        amount_sum = 0

        for item in search_results:
            if len(filter_location) > 0 and item.location != filter_location:
                continue
            if len(filter_address) > 0 and item.address != filter_address:
                continue
            if len(filter_jimok) > 0 and item.jimok != filter_jimok:
                continue
            if len(filter_usage) > 0 and item.region_usage != filter_usage:
                continue
            if len(filter_road) > 0 and item.road_length != filter_road:
                continue

            price_list.append(item)
            amount_sum = amount_sum + item.amount_per_area
            if amount_max < item.amount_per_area:
                amount_max = item.amount_per_area
            if item.amount_per_area < amount_min:
                amount_min = item.amount_per_area

    if len(price_list) > 0:
        amount_average = round(amount_sum / len(price_list))
    else:
        amount_min = 0

    #print(price_list)
    price_list.sort(key=lambda item: (item.deal_month, item.deal_day), reverse=True)

    location_code = LocationCode.objects.order_by('location')

    context = {
        'list': price_list,
        'location_code_list': location_code,
        'category_list': molit.search_category,
        'search_location': search_location,
        'search_category': search_category,
        'search_year': search_year,
        'filter_location': filter_location,
        'filter_address': filter_address,
        'filter_jimok': filter_jimok,
        'filter_usage': filter_usage,
        'filter_road': filter_road,
        'amount_average': amount_average,
        'amount_min': amount_min,
        'amount_max': amount_max,
    }

    return render(request, 'realestate/price.html', context)
