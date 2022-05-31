from django.urls import path
from graphene_django.views import GraphQLView
from .ETL.transform import clean
from .ETL.extract import scrap
from .ETL.load import load
from appartements.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    #path('', scrap)
    path('',clean),
    path('',load)

]