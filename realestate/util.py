import datetime
from json import JSONEncoder

# convert 'yyyy-mm-dd' string to datetime.date type
def yyyymmdd_to_date(value):
    if not value or len(value) != 10:
        return None
    year = int(value[0:4])
    month = int(value[5:7])
    day = int(value[8:10])
    return datetime.date(year, month, day)


class MyJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        return o.__dict__

if __name__ == "__main__":
    print(yyyymmdd_to_date('1945-01-01'))
