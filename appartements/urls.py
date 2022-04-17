from django.urls import path
from graphene_django.views import GraphQLView
from .ETL.transform import clean
from .ETL.extract import scrap
from .ETL.load import load
from appartements.schema import schema

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    #path('', scrap)
    #path('',clean)
    #path('',load)

]