import os
import pandas as pd
import pymongo
import json
from django.http import HttpResponse
import csv
from appartements.models import Appartement


def load(*args):

    url = "./appartements/DataSets/clean_house.csv"
    with open(url, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Appartement.objects.all().delete()

        for row in reader:
            print(row)

            appartement= Appartement(
                title=row[1],
                location=row[2],
                security=row[3],
                garage=row[4],
                concierge=row[5],
                city=row[7],
                currency=row[8],
                nmbr_of_rooms=row[9],
                Nmbr_of_pieces=row[10],
                Nmbr_of_bathrooms=row[11],
                condition=row[12],
                surface=row[13],
                price=row[6]
            )
            appartement.save()

    response = HttpResponse()
    response.headers['Status'] = 200
    return response

#load()
