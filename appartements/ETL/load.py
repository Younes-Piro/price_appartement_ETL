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
                title=row[1] if (row[1]) else None,
                location=row[2] if (row[2]) else None,
                security=row[3] if (row[3]) else None,
                garage=row[4] if (row[4]) else None,
                concierge=row[5] if (row[5]) else None,
                city=row[7] if (row[7]) else None,
                currency=row[8] if (row[8]) else None,
                nmbr_of_rooms=row[9] if (row[9]) else None,
                Nmbr_of_pieces=row[10] if (row[10]) else None,
                Nmbr_of_bathrooms=row[11] if (row[11]) else None,
                type=row[12] if (row[12]) else None,
                surface=row[13] if (row[13]) else None,
                price=row[6] if (row[6]) else None
            )
            appartement.save()

    response = HttpResponse()
    response.headers['Status'] = 200
    return response

load()
