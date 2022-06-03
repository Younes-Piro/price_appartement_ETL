import graphene
from .models import Appartement
from .mutation import AppartementsType, Dictionary, InnerItem
from django.db.models import Avg, Max, Min, Count
from django.db.models import FloatField
from graphene_django import DjangoListField, DjangoObjectType
import json
# query are useful to query the data from our database


class Query(graphene.ObjectType):

    all_appartements = graphene.List(AppartementsType)
    single_appartement = graphene.List(AppartementsType)
    cards = graphene.List(Dictionary)
    details_grouping = graphene.List(Dictionary)

    # details of pricing

    def resolve_cards(self, info):
        example_dict = {
            "NUMBER APPARTEMENT": {"value": Appartement.objects.aggregate(Count('price')).get('price__count')},
            "MINIMAL PRICE": {"value": Appartement.objects.aggregate(Min('price')).get('price__min')},
            "AVERAGE PRICE": {"value": Appartement.objects.aggregate(Avg('price')).get('price__avg')},
            "MAX PRICE": {"value": Appartement.objects.aggregate(Max('price')).get('price__max')}
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

        diction = Appartement.objects.values('city').annotate(
            avg_rooms=Avg('nmbr_of_rooms'),
            avg_surface=Avg('surface')
        ).order_by()

        Dict = {}
        for single_dic in diction:
            Dict[single_dic.get('city')] = single_dic

        results = []        # Create a list of Dictionary objects to return
        # Now iterate through your dictionary to create objects for each item
        for key, value in Dict.items():
            inner_item = InnerItem(
                value['avg_rooms'], value['avg_surface'])
            dictionary = Dictionary(key, inner_item)
            results.append(dictionary)

        return results

    def resolve_single_appartement(self, info, **kwargs):
        return Appartement.objects.total_price().first()

    def resolve_all_appartements(self, info, **kwargs):
        return Appartement.objects.all()


# importing the schema
schema = graphene.Schema(query=Query)
