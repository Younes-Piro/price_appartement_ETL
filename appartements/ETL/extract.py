from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
from django.http import HttpResponse

def scrap(*args):
    titles=[]
    prices=[]
    descriptions = []
    locations = []
    securities = []
    terraces = []
    garages = []
    concierges = []
    text = ""

    cities = ['rabat','marrakech','agadir','casablanca','f%C3%A8s','tanger']
    for city in cities:
        for i in range(0,40):
            #url
            page = f'https://www.mubawab.ma/fr/ct/{city}/immobilier-a-vendre:p:{i}'

            #agent for real simulation
            USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
            LANGUAGE = "en-US,en;q=0.5"
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            session.headers['Accept-Language'] = LANGUAGE
            session.headers['Content-Language'] = LANGUAGE

            #souping
            response = session.get(page).text
            soup = bs(response, 'html.parser')
            houses_list = soup.find_all('li', class_= lambda x: x != 'adBoostBox' and x=='listingBox')
            for single_house in houses_list:
                url = single_house['linkref']
                new_response = requests.get(url)
                soup2 = bs(new_response.content, 'html.parser')
                general_infos = soup2.find_all('div',{'class':'floatR'}) 

                for info in general_infos:
                    
                    feature = info.find_all("span" , class_="tagProp")
                
                    for f in feature:
                        text +=  f.text.strip() + "//"
                    
                    if info.find('h1',{'class':'searchTitle'}) == None:
                        title = None
                    else:
                        title = info.find('h1',{'class':'searchTitle'}).text.strip() 

                    
                    if info.find('h3',{'class':'orangeTit'}) == None:
                        price = None
                    else:
                        price = info.find('h3',{'class':'orangeTit'}).text.strip()
                    
                    

                    if info.find('h3',{'class':'greyTit'}) == None:
                        location = None
                    else:
                        location = info.find('h3',{'class':'greyTit'}).text.strip()

                    characteristics = info.find_all('div',{"class": "characLinkBox"})
                    for characteristic in characteristics:
                        if characteristic.find('div',{"id": "terraceLink"}) == None :
                            terrace = 0
                        else:
                            terrace = 1
                        if characteristic.find('div',{"id": "doormanLink"}) == None :
                            concierge = 0
                        else:
                            concierge = 1
                        if characteristic.find('div',{"id": "securityLink"}) == None :
                            security = 0
                        else:
                            security = 1
                        if characteristic.find('div',{"id": "garageLink"}) == None :
                            garage = 0
                        else:
                            garage = 1

                    locations.append(location)
                    prices.append(price)
                    titles.append(title)
                    securities.append(security)
                    garages.append(garage)
                    concierges.append(concierge)
                    descriptions.append(text)
                    text = ""

    file = pd.DataFrame({"Title":titles,
                        "Location":locations,
                        "Security":securities,
                        "Garage" : garages,
                        "Concierge":concierges,
                        "Description":descriptions,
                        "Price":prices
                        })

    file.to_csv('.appartements/Datasets/house.csv')
    response = HttpResponse()
    response.headers['Status'] = 200
    return response


#calling the function
#scrap()


            
