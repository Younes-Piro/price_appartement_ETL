import graphene
from .models import Appartement
from graphene_django import DjangoListField, DjangoObjectType


class AppartementsType(DjangoObjectType): #serialisation the data from our model to graphql
    class Meta:
        model = Appartement
        fields = "__all__"
