import json
from datetime import datetime
import random
import os

file_path = "../data/june1-15.json"


def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def load_data_filter(status):
    f = open(file_path)
    data = json.load(f, strict=False)
    lst = data["data"]["analyticsRequestByParams"]
    filtered_list = []
    print(f"Total records {len(lst)}")
    for item in lst:
        if item['status'] == status:
            filtered_list.append(item)
    print(f"With status {status} has found {len(filtered_list)} records")
    return filtered_list


def generate_data_between(date_lst):
    lst = load_data_filter('INQ_RESP')
    month_dict = {1: 'Jan', 2: 'Feb',
                  3: 'Mar', 4: 'Apr',
                  5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug',
                  9: 'Sep', 10: 'Oct',
                  11: 'Nov', 12: 'Dec'}
    for i in date_lst:
        mm_yyyy = i.split("-")
        month = int(mm_yyyy[0])
        year = int(mm_yyyy[1])
        data_list = []
        id_list = list(get_id(len(lst), year, month))
        i = 0
        for item in lst:
            item['id'] = id_list[i]
            item['actionTimestamp'] = format_date(item['actionTimestamp'], month, year)
            item['createdTime'] = format_date(item['createdTime'], month, year)
            item['requestedDatetime'] = format_date(item['requestedDatetime'], month, year)
            item['statusUpdateDatetime'] = format_date(item['statusUpdateDatetime'], month, year)
            payload = json.loads(item["payload"])
            payload['reqDateTime'] = format_date(payload['reqDateTime'], month, year)
            payload['additionalInfo']['actionTimestamp'] = format_date(payload['additionalInfo']['actionTimestamp'],
                                                                       month, year)
            payload['lastActionDateTime'] = format_date(payload['lastActionDateTime'], month, year)
            item['payload'] = json.dumps(payload)
            data_list.append(item)
            i = i + 1
        file_name = f"../output/{month_dict[month]}_{year}.json"
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_name, 'w') as f:
            final_data = {'data': {'analyticsRequestByParams': data_list}}
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
        id_set.add(f"{str(year)[2:]}{month}{first + random.randint(size, size * 3) + second}")
    return id_set


if __name__ == '__main__':
    generate_data_between(["01-2024"])
