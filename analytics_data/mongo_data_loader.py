import pymongo
import json
#myclient = pymongo.MongoClient("mongodb://devuser:devuser!23@localhost:27017/m360_dev_db")

myclient = pymongo.MongoClient("mongodb://devuser:devuser!23@10.18.129.125:27017/m360_dev_db")
mydb = myclient["m360_dev_db"]


def load_analytics_agg_data(fileName):
    mycol = mydb["analytics_request_agg_data"]
    with open(f'../output/agg-data/{fileName}', 'r') as file:
         data = json.load(file)
         lst = data["data"]["analyticsAggregatedRequestByParams"]
         print(len(lst))
         count = 1
         data_list = []
         for ele in lst:
             print(f"Count :{count}")
             record = {}
             record["data"] = ele
             data_list.append(record)
             count = count + 1
         mycol.insert_many(data_list)


def load_analytics_request_data(fileName):
    mycol = mydb["analytics_request_data"]
    with open(f'../output/{fileName}', 'r') as file:
         data = json.load(file)
         lst = data["data"]["analyticsRequestByParams"]
         print(len(lst))
         count = 1
         data_list = []
         for ele in lst:
             print(f"Count :{count}")
             record = {}
             record["data"] = ele
             data_list.append(record)
             count = count + 1
         mycol.insert_many(data_list)



load_analytics_agg_data('Jan_2024_agg.json')
load_analytics_request_data('Jan_2024.json')
