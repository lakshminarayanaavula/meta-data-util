import json
from datetime import datetime
import random
import os

file_path = "../data/Aggregated1-15.json"


def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def get_agg_data():
    f = open(file_path)
    data = json.load(f, strict=False)
    lst = data["data"]["analyticsAggregatedRequestByParams"]
    print(f"Aggregated data size {len(lst)}")
    return lst


def generate_data_between(date_lst):
    lst = get_agg_data()
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',11: 'Nov', 12: 'Dec'}
    random.sample(range(10000, 100000), len(lst))
    for i in date_lst:
        mm_yyyy = i.split("-")
        month = int(mm_yyyy[0])
        year = int(mm_yyyy[1])
        data_list = []
        id_list = list(get_id(len(lst), year, month))
        i = 0
        for item in lst:
            item['id'] = id_list[i]
            item['createdTime'] = format_date(item['createdTime'], month, year)
            item['reportStartTime'] = format_date(item['reportStartTime'], month, year)
            item['reportEndTime'] = format_date(item['reportEndTime'], month, year)
            item['createdTime'] = format_date(item['createdTime'], month, year)
            item['insertedOn'] = format_date(item['insertedOn'], month, year)
            payload = json.loads(item["payload"])
            payload['reqDateTime'] = format_date(payload['reqDateTime'], month, year)
            payload["additionalInfo"]['report_start_time'] = format_date(payload["additionalInfo"]['report_start_time'], month, year)
            if payload["additionalInfo"].get('requestCreationDate'):
                payload["additionalInfo"]['requestCreationDate'] = format_date(payload["additionalInfo"]['requestCreationDate'], month, year)
            payload['lastActionDateTime'] = format_date(payload['lastActionDateTime'], month, year)
            item['payload'] = json.dumps(payload)
            data_list.append(item)
            i = i + 1
        file_name = f"../output/agg-data/{month_dict[month]}_{year}_agg.json"
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_name, 'w') as f:
           final_data = {'data': {'analyticsAggregatedRequestByParams': data_list}}
           json.dump(json.loads(json.dumps(final_data, ensure_ascii=True, indent=4)), f, indent=1)


def format_date(date_str, month, year):
    if len(date_str) > 19:
        date_str = date_str[0:19]
    try:
        created_date = datetime.fromisoformat(date_str).replace(month=month, year=year)
        res = created_date.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        day = 30
        if month == 2:
            if is_leap_year(year):
                day = 29
            else:
                day = 28
        created_date = datetime.fromisoformat(date_str).replace(month=month, year=year, day=day)
        res = created_date.strftime("%Y-%m-%dT%H:%M:%S")
    return res


def get_id(size, year, month):
    id_set = set()
    prime = [2, 3, 5, 7]
    while len(id_set) != size:
        first = prime[random.randint(0, 3)]
        second = prime[random.randint(0, 3)]
        id_set.add(f"{str(year)[2:]}{month}{first+random.randint(size, size * 3)+second}")
    return id_set


if __name__ == '__main__':
    generate_data_between(["01-2024"])