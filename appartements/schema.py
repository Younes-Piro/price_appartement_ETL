import graphene
from .models import Appartement
from .mutation import AppartementsType, Dictionary, InnerItem
from django.db.models import Avg, Max, Min, Count
from django.db.models import FloatField
from graphene_django import DjangoListField, DjangoObjectType
import json
# query are useful to query the data from our database

class Query(graphene.ObjectType):

    all_appartements = graphene.List (AppartementsType)
    single_appartement = graphene.List(AppartementsType)
    cards = graphene.List(Dictionary) 
    details_grouping = graphene.List(Dictionary) 



    # details of pricing
    def resolve_cards(self, info):
        example_dict = {
            "NUMBER APPARTEMENT" : {"value": Appartement.objects.aggregate(Count('price')).get('price__count') },
            "MINIMAL PRICE" : {"value": Appartement.objects.aggregate(Min('price')).get('price__min') },
            "AVERAGE PRICE" : {"value": Appartement.objects.aggregate(Avg('price')).get('price__avg') },
            "MAX PRICE" : {"value": Appartement.objects.aggregate(Max('price')).get('price__max') }
        }

        results = []        # Create a list of Dictionary objects to return

        # Now iterate through your dictionary to create objects for each item
        for key, value in example_dict.items():
            inner_item = InnerItem(value['value'])
            dictionary = Dictionary(key, inner_item)
            results.append(dictionary)

        return results

    # details after grouping
    def resolve_details_grouping(self, info):
        
        example_dict = {
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[0].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[0].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[0].get('surface__avg'),
                } ,
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[1].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[1].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[1].get('surface__avg'),
                } ,
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[2].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[2].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[2].get('surface__avg'),
                } ,
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[3].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[3].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[3].get('surface__avg'),
                } ,
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[4].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[4].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[4].get('surface__avg'),
                } ,
            Appartement.objects.values('city').annotate(count=Avg('nmbr_of_rooms'))[5].get('city') : {
                "AVERAGE NUMBERS OF ROOMS":Appartement.objects.values('city').annotate(Avg('price'))[5].get('price__avg'),
                "AVERAGE SURFACE":Appartement.objects.values('city').annotate(Avg('surface'))[5].get('surface__avg'),
                } ,
        }
        results = []        # Create a list of Dictionary objects to return
        # Now iterate through your dictionary to create objects for each item
        for key, value in example_dict.items():
            inner_item = InnerItem(value['AVERAGE NUMBERS OF ROOMS'],value['AVERAGE SURFACE'])
            dictionary = Dictionary(key, inner_item)
            results.append(dictionary)

        return results

    def resolve_single_appartement(self, info, **kwargs):
        return Appartement.objects.total_price().first()

    def resolve_all_appartements(self, info , **kwargs):
        return Appartement.objects.all()


# importing the schema
schema = graphene.Schema(query=Query)