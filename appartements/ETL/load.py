import os
import pandas as pd
import pymongo
import json
from django.http import HttpResponse

def load(*args):

    url = "./appartements/DataSets/clean_house.csv"
    df = pd.read_csv(url,index_col=[0])


    client = pymongo.MongoClient("mongodb://localhost:27017")
    data = df.to_dict (orient = "records")
    db = client["appartements"]
    db.table.insert_many(data)

    response = HttpResponse()
    response.headers['Status'] = 200
    return response

load()