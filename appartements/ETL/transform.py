import pandas as pd
import numpy as np
from django.http import HttpResponse
import csv

def clean(*args):
    url = "./appartements/DataSets/house.csv"
    df = pd.read_csv(url,index_col=[0])
    
    ##droping nan values in title location and description
    df.dropna(subset = ['Title', 'Location', 'Description'], inplace = True)
    df.reset_index(drop=True, inplace=True)

    #geting the city from each location by getting the last element of the list
    def get_city(data):
        return data.replace('\n', '').replace('\t', '').split(' ')[-1]

    df['City'] = df['Location'].apply(lambda x : get_city(x))

    #reformating the city by deleting à in the beginning of each city
    def format_city(data):
        if data[0] == 'à':
            return data[1:]
        else:
            return data
    df['City'] = df['City'].apply(lambda x : format_city(x))

    ## getting every location exactling without the City
    df["Location"] = df["Location"].apply(lambda x : x.split('à')[0])


    ###### dealing with price

    #replacing spaces
    def replice_price(data):
        if isinstance(data, str):
            return data.replace(u'\xa0', u'').replace(u'E', u'')
        else:
            return data

    df["Price"] = df["Price"].apply(lambda x : replice_price(x))

    ##geting the currency
    df["Currency"] = df["Price"].str[-2:]
    df["Price"] = df["Price"].str[:-2]

    ###### dealing with description

    data = df.copy()

    # slicing data to list of features

    def sliting(data):
        return data.split('//')

    data["Description"] = data["Description"].apply(lambda x : sliting(x))

    #filtering every piece bathroom ..
    def get_data(data,filtre1,filtre2):
        for item in data:
            if filtre1 in item or filtre2 in item:
                return item
            else:
                pass

    data["Nmbr_rooms"] = data["Description"].apply(lambda x : get_data(x,'Chambres','Chambre'))
    data["Nmbr_pieces"] = data["Description"].apply(lambda x : get_data(x,'Pièce','Pièces'))
    data["Nmbr_bathrooms"] = data["Description"].apply(lambda x : get_data(x,'Salle','Salles'))

    #addind third filter for types
    def get_type(data,filtre1,filtre2,filtre3):
        for item in data:
            if filtre1 in item or filtre2 in item or filtre3 in item:
                return item
            else:
                pass

    data["Type"] = data["Description"].apply(lambda x : get_type(x,'Nouveau','Bon état',"À rénover"))            


    #getting the surface of every appartement
    def get_surface(data):
        for item in data:
            if 'm²' in item:
                return item
            else:
                pass
        
    data["Surface"] = data["Description"].apply(lambda x: get_surface(x))

    # replacing spaces
    def get_surface(data):
        if data == None:
            return np.nan
        else:
            return data.replace('\n', '').replace('\t', '')

    data["Surface"] = data["Surface"].apply(lambda x: get_surface(x))

    #geting exaclty the numbers from every feature
    def get_nmbr(data):
        if data == None:
            return None
        else:
            return data.split(' ')[0]

    data["Nmbr_rooms"] = data["Nmbr_rooms"].apply(lambda x: get_nmbr(x))
    data["Nmbr_bathrooms"] = data["Nmbr_bathrooms"].apply(lambda x: get_nmbr(x))
    data["Nmbr_pieces"] = data["Nmbr_pieces"].apply(lambda x: get_nmbr(x))

    #droping column of description
    data.drop('Description', inplace=True, axis=1)
    data.reset_index(drop=True, inplace=True) ## reseting indexes

    ## fill the null values with mode in discret variables
    data['Nmbr_rooms'] = data['Nmbr_rooms'].fillna(data['Nmbr_rooms'].mode()[0])
    data['Nmbr_pieces'] = data['Nmbr_pieces'].fillna(data['Nmbr_pieces'].mode()[0])
    data['Nmbr_bathrooms'] = data['Nmbr_bathrooms'].fillna(data['Nmbr_bathrooms'].mode()[0])
    data['Type'] = data['Type'].fillna(data['Type'].mode()[0])
    data['Surface'] = data['Surface'].fillna(data['Surface'].mode()[0])

    #formating variables
    data['Nmbr_rooms'] = data['Nmbr_rooms'].astype(int)
    data['Nmbr_pieces'] = data['Nmbr_pieces'].astype(int)
    data['Nmbr_bathrooms'] = data['Nmbr_bathrooms'].astype(int)


    data["Surface"] = data["Surface"].astype(str)
    data["Surface"] = data["Surface"].apply(lambda x : None if (x == None) else x[:-2]) 
    data['Surface'] = data['Surface'].astype(int)

    data["Price"] = data["Price"].astype('float') 
    df2 = data.loc[~df['Title'].str.contains('Villa', 'villa')]
    df2 = df2.dropna()

    #Price*Surface (foreach price < 15K)

    df2.loc[df2['Price'] < 150000 , ['Price']] = df2['Price']*df2['Surface']

    df2.loc[df2['Currency'] == 'UR' , ['Price']] = df2['Price']*10
    df2.loc[df2['Currency'] == 'UR' , ['Currency']] = 'DH'
    df2.to_csv("./appartements/DataSets/clean_house.csv")
    
    response = HttpResponse()
    response.headers['Status'] = 200
    return response

#clean()