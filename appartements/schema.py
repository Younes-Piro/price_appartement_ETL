import graphene
from .models import Appartement
from .mutation import AppartementsType, Dictionary, InnerItem
from django.db.models import Avg, Max, Min, Count
from django.db.models import FloatField
from graphene_django import DjangoListField, DjangoObjectType
import json
# query are useful to query the data from our database

class Query(graphene.ObjectType):

    all_appartement = graphene.Field(AppartementsType)
    single_appartement = graphene.List(AppartementsType)
    details = graphene.List(Dictionary) 
    details_grouping = graphene.List(Dictionary) 



    # details of pricing
    def resolve_details(self, info):
        example_dict = {
            "MAX_PRICE" : {"value": Appartement.objects.aggregate(Max('price')).get('price__max') },
            "MIN_PRICE" : {"value": Appartement.objects.aggregate(Min('price')).get('price__min') },
            "AVG_PRICE" : {"value": Appartement.objects.aggregate(Avg('price')).get('price__avg') }
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
            "MAX_PRICE_1" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[0] ,
            "MAX_PRICE_2" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[1] ,
            "MAX_PRICE_3" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[2] ,
            "MAX_PRICE_4" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[3] ,
            "MAX_PRICE_5" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[4] ,
            "MAX_PRICE_6" : Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[5] ,

        }
        results = []        # Create a list of Dictionary objects to return
        # Now iterate through your dictionary to create objects for each item
        for key, value in example_dict.items():
            inner_item = InnerItem(value['dcount'],value['city'])
            dictionary = Dictionary(key, inner_item)
            results.append(dictionary)

        return results

    def resolve_single_appartement(self, info, **kwargs):
          
        # serializer_class = AppartementsType
        # queryset = Appartement.objects.aggregate(Max('nmbr_of_rooms'))
        # return queryset
        # client = MongoClient(host="localhost", port=27017)
        # db = client.housy
        # return DjangoObjectType.get_queryset(queryset=db.appartements_appartement.find({"city":"Rabat"}),info="")
        return Appartement.objects.total_price().first()

    def resolve_all_appartement(self, info , **kwargs):
        return (
            Appartement.objects.values('city').annotate(dcount=Avg('nmbr_of_rooms'))[0]
        )

# importing the schema
schema = graphene.Schema(query=Query)