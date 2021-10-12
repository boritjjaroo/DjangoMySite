import datetime
from django.shortcuts import render

from ..models import *
from ..ItemInfo import *
import gov.molit as molit
from gov.nsdi.building import BuildingInfo

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

def price_search(request):
    result_list = []
    search_location = request.POST.get('search_location')
    search_bonbun = request.POST.get('search_bonbun')
    search_bubun = request.POST.get('search_bubun')
    search_year = request.POST.get('search_year')
    search_area = request.POST.get('search_area')
    if search_area:
        search_area_f = float(search_area)
    else:
        search_area_f = None
    location_codes = LocationCode.objects.order_by('location')
    if search_location:
        location_code = location_codes.get(code=search_location)
    else:
        location_code = None
    if location_code:
        search_address = location_code.location
    else:
        search_address = ''

    search_results = BuildingInfo.search(search_location, 0, search_bonbun, search_bubun)

    for item in search_results:
        # 단독주택
        if item.main_purpose_cd != '01000':
            continue
        if search_year and item.use_date and not item.use_date.startswith(search_year):
            continue
        if search_area_f and item.plot_area:
            if item.plot_area < search_area_f * 0.98 or search_area_f * 1.02 < item.plot_area:
                continue
        result_list.append(item)

    result_list.sort(key=lambda item: (item.jibun))


    context = {
        'list': result_list,
        'location_code_list': location_codes,
        'search_location': search_location,
        'search_address': search_address,
        'search_bonbun': search_bonbun,
        'search_bubun': search_bubun,
        'search_year': search_year,
        'search_area': search_area,
    }

    return render(request, 'realestate/price_search.html', context)
