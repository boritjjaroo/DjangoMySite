from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import time
import json
import os
import datetime
from decimal import *

from ..models import *
from ..ItemInfo import *
from ..util import *
import naver.land as nl
import naver.map as nm
import gov.molit as molit
from gov.nsdi.price import HousePrice


json_save_path = './realestate/json'
land_image_path = './static/pic/realestate'
land_file_path = './static/file/realestate'

def index(request):
    result_list = []
    realestate_list = Realestate.objects.filter(is_favorite=True).order_by('address_jibun')

    for item in realestate_list:
        my_list = MyLandItem.objects.filter(realestate_id=item.id).order_by('article_no')
        iteminfo = ItemInfo2()
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

def alllist(request):
    result_list = []
    realestate_list = Realestate.objects.order_by('address_jibun')

    for item in realestate_list:
        #my_list = MyLandItem.objects.filter(realestate_id=item.id).order_by('article_no')
        iteminfo = ItemInfo2()
        iteminfo.realestate = item
        #iteminfo.mylist = my_list
        result_list.append(iteminfo)

    context = { 'list': result_list }
    return render(request, 'realestate/all_list.html', context)

def declared_get(request):
    result = 'Fail'
    address = ''
    price_infos = None
    try:
        item_id = request.POST.get('item_id')
        realestate = Realestate.objects.get(id=item_id)
        address = realestate.address_jibun
        addr_info = nm.addr_search(realestate.address_jibun)
        jibuns = addr_info.jibun.split('-')
        bonbun = int(jibuns[0])
        if 1 < len(jibuns):
            bubun = int(jibuns[1])
        else:
            bubun = 0
        #print(f'{realestate.lawd_cd}, {bonbun}, {bubun}')
        price_infos = HousePrice.search(realestate.lawd_cd, 0, bonbun, bubun, 2021)
        #print(len(price_infos))
        if len(price_infos):
            result = 'Success'
    except Exception as e:
        print('alllist_declared() exception!', e)
        pass

    context = { 'result': result, 'address': address, 'list': price_infos }
    json_data = json.dumps(context, cls=MyJsonEncoder, ensure_ascii=False)
    #print(json_data)
    return HttpResponse(json_data, content_type="application/json")

def declared_update(request):
    result = 'Fail'
    try:
        item_id = request.POST.get('item_id')
        date = request.POST.get('date')
        price = request.POST.get('price')
        realestate = Realestate.objects.get(id=item_id)
        realestate.declared_value = price
        realestate.declared_value_date = yyyymmdd_to_date(date)
        realestate.save()
        result = 'Success'
    except:
        pass

    context = { 'result': result }
    return HttpResponse(json.dumps(context), content_type="application/json")

def detail(request, listitem_id):
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

        naver_item = NaverItem()
        naver_item.naver = land_item
        result_list.append(naver_item)
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

            land_item = nl.LandItem()
            json_file_path = f'{json_save_path}/{nl.LandItem.getJsonFileNameS(my_item.article_no,my_item.article_confirm_ymd)}'
            # 이미 저장된 아이템일 경우 json 파일 읽기
            if land_item.loadJson(json_file_path) == False:
                # 신규 또는 확인날짜가 바뀌었을 경우 상세정보 json 파일 다운로드
                time.sleep(0.3)
                land_item.parseFromID(my_item.article_no)
                land_item.saveJson(json_save_path)

            naver_item = NaverItem()

            if 0 < my_item.realestate_id:
                naver_item.realestate = Realestate.objects.get(id=my_item.realestate_id)
                # 단독only 조건일 경우 다가구 제외        
                if is_building_type_ddonly and not naver_item.realestate.is_dandok:
                    continue
            else:
                realestate_list = Realestate.objects.filter(address_jibun=land_item.address)
                if 0 < len(realestate_list):
                    naver_item.realestate_match = realestate_list.first()
                    # 단독only 조건일 경우 다가구 제외        
                    #if is_building_type_ddonly and not naver_item.realestate_match.is_dandok:
                    #    continue
                
            naver_item.naver = land_item
            naver_item.myitem = my_item
            result_list.append(naver_item)

    result_list.sort(key=lambda item: item.naver.address)

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

def naver_register(request):
    item_id = request.GET.get('item_id')
    my_item = MyLandItem.objects.get(id=item_id)
    article_no = my_item.article_no
    article_confirm_ymd = my_item.article_confirm_ymd

    json_file_path = f'{json_save_path}/{nl.LandItem.getJsonFileNameS(article_no,article_confirm_ymd)}'
    land_item = nl.LandItem()
    land_item.loadJson(json_file_path)

    addr_info = nm.addr_search(land_item.address)
    jibuns = addr_info.jibun.split('-')
    bonbun = jibuns[0]
    if 1 < len(jibuns):
        bubun = jibuns[1]
    else:
        bubun = ''
    price_infos = HousePrice.search(addr_info.lawd_cd, 0, bonbun, bubun)

    realestate = Realestate()
    realestate.address_jibun = land_item.address
    realestate.address_road = addr_info.address_road
    realestate.lawd_cd = addr_info.lawd_cd
    realestate.area = land_item.area
    realestate.building_area = land_item.building_area
    realestate.total_floor_area = land_item.total_floor_area
    appdate = land_item.getUseApproveDate()
    if appdate:
        realestate.use_approval_date = datetime.date(appdate.year, appdate.month, appdate.day)
    realestate.structure = land_item.structure
    realestate.heating = land_item.heating
    #realestate.sewage
    if 0 < len(price_infos):
        realestate.declared_value = price_infos[0].price
        realestate.declared_value_date = price_infos[0].date
    #realestate.deal_price
    #realestate.deal_date
    #realestate.is_favorite
    #realestate.is_dandok
    #realestate.memo
    #realestate.file_prefix

    context = {
        'realestate': realestate,
        'item_id': item_id
    }
    return render(request, 'realestate/naver_register.html', context)

def naver_register_action(request):
    realestate = Realestate(address_jibun='')

    realestate.address_jibun = request.POST.get('address_jibun', '')
    realestate.address_road = request.POST.get('address_road', '')
    realestate.lawd_cd = request.POST.get('lawd_cd', '')
    realestate.area = Decimal(request.POST.get('area', '0.0'))
    realestate.building_area = Decimal(request.POST.get('building_area', '0.0'))
    realestate.total_floor_area = Decimal(request.POST.get('total_floor_area', '0.0'))
    use_approval_date = request.POST.get('use_approval_date', '')
    realestate.use_approval_date = yyyymmdd_to_date(use_approval_date)
    realestate.structure = request.POST.get('structure', '')
    realestate.heating = request.POST.get('heating', '')
    realestate.sewage = request.POST.get('sewage', '')
    realestate.declared_value = request.POST.get('declared_value', '')
    declared_value_date = request.POST.get('declared_value_date', '')
    realestate.declared_value_date = yyyymmdd_to_date(declared_value_date)
    realestate.deal_price = 0
    realestate.deal_date = None
    realestate.is_favorite = 'is_favorite' in request.POST
    realestate.is_dandok = 'is_dandok' in request.POST
    realestate.memo = request.POST.get('memo', '')
    realestate.file_prefix = request.POST.get('file_prefix', '')

    realestate.save()

    item_id = request.POST.get('item_id')
    my_item = MyLandItem.objects.get(id=item_id)
    my_item.realestate_id = realestate.id
    my_item.is_new = False
    my_item.save()

    return HttpResponse('완료')

def naver_link(request):
    result = 'Fail'
    try:
        item_id = request.POST.get('item_id')
        realestate_id = request.POST.get('match_id')
        my_item = MyLandItem.objects.get(id=item_id)
        my_item.is_new = False
        my_item.realestate_id = realestate_id
        my_item.save()
        result = 'Success'
    except:
        pass

    context = { 'result': result }
    return HttpResponse(json.dumps(context), content_type="application/json")

def check(request):
    result = 'Fail'
    try:
        item_id = request.POST.get('item_id')
        my_item = MyLandItem.objects.get(id=item_id)
        my_item.is_new = False
        my_item.save()
        result = 'Success'
    except:
        pass

    context = { 'result': result }
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
            # 검색 조건 필터링
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

            price_info = PriceInfo()
            price_info.price = item

            # 실제 대상물 검색
            deal_date = datetime.date(int(search_year), item.deal_month, item.deal_day)
            realestates = Realestate.objects.filter(deal_price=item.amount, deal_date=deal_date)
            if 0 < len(realestates):
                price_info.realestate = realestates[0]
            price_list.append(price_info)

            # 최소, 최대, 평균금액 계산
            amount_sum = amount_sum + item.amount_per_area
            if amount_max < item.amount_per_area:
                amount_max = item.amount_per_area
            if item.amount_per_area < amount_min:
                amount_min = item.amount_per_area

    # 최소, 최대, 평균금액 계산
    if len(price_list) > 0:
        amount_average = round(amount_sum / len(price_list))
    else:
        amount_min = 0

    #print(price_list)
    price_list.sort(key=lambda item: (item.price.deal_month, item.price.deal_day), reverse=True)

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
