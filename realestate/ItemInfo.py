from .models import Realestate

class ItemInfo:
    def __init__(self):
        id = 0
        parent_id = 0
        image_path = ''
        article_no = ''
        article_confirm_ymd = ''
        price = 0
        initial_price = ''
        price_per_area = 0
        area = 0.0
        building_area = 0.0
        total_floor_area = 0.0
        address = ''
        build_years = 0
        memo = ''
        count = 0
        declared_value = 0
        declared_value_date = None

class ItemInfo2:
    def __init__(self):
        realestate = None
        mylist = []