from django.shortcuts import render

from gov.nsdi.building import BuildingInfo
from gov.data.bldrgs import BldRgsTitle
from gov.data.archown import ArchOwn


def search(request):
    result_list = []
    search_lawd_cd = request.POST.get('search_lawd_cd', '')
    search_bonbun = request.POST.get('search_bonbun', '')
    search_bubun = request.POST.get('search_bubun', '')

    if search_lawd_cd and len(search_lawd_cd) == 10 and search_bonbun:
        if '*' in search_bonbun:
            result_list = BuildingInfo.search(search_lawd_cd, 0, search_bonbun, search_bubun)
        else:
            result_list = BldRgsTitle.search(search_lawd_cd, 0, search_bonbun, search_bubun)

    context = {
        'list': result_list,
        'search_lawd_cd': search_lawd_cd,
        'search_bonbun': search_bonbun,
        'search_bubun': search_bubun,
    }

    return render(request, 'realestate/search.html', context)


def bldinfo(request):
    search_pnu = request.GET.get('pnu')
    owners = []

    if search_pnu:
        lawd_cd = search_pnu[0:10]
        is_san = int(search_pnu[10:11]) - 1
        bonbun = int(search_pnu[11:15])
        bubun = int(search_pnu[15:19])
        owners = ArchOwn.search(lawd_cd, is_san, bonbun, bubun)

    context = {
        'search_pnu': search_pnu,
        'owners': owners,
    }

    return render(request, 'realestate/bldinfo.html', context)
