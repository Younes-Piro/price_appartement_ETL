import pandas as pd
import numpy as np
from django.http import HttpResponse
import csv

def clean(*args):
    url = "./appartements/DataSets/house.csv"
    df = pd.read_csv(url,index_col=[0])
    
    ##droping nan values
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)

    # spliting data
    def get_city(data):
        return data.replace('\n', '').replace('\t', '').split(' ')[-1]

    df['City'] = df['Location'].apply(lambda x : get_city(x))

    def format_city(data):
        if data[0] == 'à':
            return data[1:]
        else:
            return data
    df['City'] = df['City'].apply(lambda x : format_city(x))

    def get_location(data):
        if len(data.split(' '))>1:
            return data.split(' ')[0:2]
        else: 
            return data

    df["Location"] = df["Location"].apply(lambda x : get_location(x))

    def exact_location(data):
        cities = ['Rabat','Marrakech','Agadir','Casablanca','F%C3%A8s']
        for city in cities :
            if(data[1] == f"à\n\t\t\t\t{city}" or data[1] == '1'):
                return data[0]
            else:
                return f"{data[0]} {data[1]}"
    df["Location"] = df["Location"].apply(lambda x : exact_location(x))

    ###### dealing with price

    df["Price"] = df["Price"].apply(lambda x : x.replace(u'\xa0', u''))
    df["Currency"] = df["Price"].str[-2:]
    df["Price"] = df["Price"].str[:-2]
    df["Price"] = df["Price"].apply(lambda x : x.replace(u'E', u''))
    df["Price"] = df["Price"].astype(int)

    ###### dealing with description

    data = df.copy()

    def sliting(data):
        return data.split('//')

    data["Description"] = data["Description"].apply(lambda x : sliting(x))
    data['Length'] = data['Description'].str.len()
    data = data.loc[data['Length'] > 3]

    def nmbr_bathroom(data):
        if len(data.split(' '))>1:
            if (data.split(' ')[1]) == "Chambre" or (data.split(' ')[1]) == "Chambres":
                return data
            else:
                return None
        else:
            return None
            
    data["Nmbr of rooms"] = data["Description"].apply(lambda x : nmbr_bathroom(x[2]))

    def nmbr_bathroom(data):
        if len(data.split(' '))>1:
            if (data.split(' ')[1]) == "Pièce" or (data.split(' ')[1]) == "Pièces":
                return data
            else:
                return None
        else:
            return None
            
    data["Nmbr of pieces"] = data["Description"].apply(lambda x : nmbr_bathroom(x[1]))

    def nmbr_bathroom(data):
        if len(data.split(' '))>1:
            if (data.split(' ')[1]) == "Salle" or (data.split(' ')[1]) == "Salles":
                return data
            else:
                return None
        else:
            return None
            
    data["Nmbr of bathrooms"] = data["Description"].apply(lambda x : nmbr_bathroom(x[3]))

    def check_newness(data1, data2):
        if len(data1.split(' '))>1:
            if (data1.split(' ')[1]) == "Salle" or (data1.split(' ')[1]) == "Salles":
                if data2 not in ["Nouveau","Bon état","À rénover"]:
                    return None
                else:
                    return data2
            else:
                if data1 not in ["Nouveau","Bon état","À rénover"]:
                    return None
                else:
                    return data1
        else:
            if data1 not in ["Nouveau","Bon état","À rénover"]:
                return None
            else:
                return data1
    data["Newness"] = data["Description"].apply(lambda x : check_newness(x[3],x[4]))

    data["Surface"] = data["Description"].apply(lambda x: x[0])
    def get_surface(data):
        return data.replace('\n', '').replace('\t', '')
    data["Surface"] = data["Surface"].apply(lambda x: get_surface(x))
    data["Surface"] = data["Surface"].str[:-2]

    def get_nmbr(data):
        if data == None:
            return None
        else:
            return data.split(' ')[0]

    data["Nmbr of rooms"] = data["Nmbr of rooms"].apply(lambda x: get_nmbr(x))
    data["Nmbr of pieces"] = data["Nmbr of pieces"].apply(lambda x: get_nmbr(x))
    data["Nmbr of bathrooms"] = data["Nmbr of bathrooms"].apply(lambda x: get_nmbr(x))
    data.drop('Description', inplace=True, axis=1)
    data.drop('Length', inplace=True, axis=1)
    data = data.dropna()
    data.reset_index(drop=True, inplace=True)

    data["Nmbr of rooms"] = data["Nmbr of rooms"].astype('int64')
    data["Nmbr of pieces"] = data["Nmbr of pieces"].astype('int64')
    data["Nmbr of bathrooms"] = data["Nmbr of bathrooms"].astype('int64')

    data.to_csv("./appartements/DataSets/clean_house.csv")
    response = HttpResponse()
    response.headers['Status'] = 200
    return response


#clean()