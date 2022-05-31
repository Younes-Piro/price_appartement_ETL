import graphene
from .models import Appartement
from graphene_django import DjangoListField, DjangoObjectType


class AppartementsType(DjangoObjectType): #serialisation the data from our model to graphql
    class Meta:
        model = Appartement
        fields = "__all__"

# Our inner dictionary defined as an object
class InnerItem(graphene.ObjectType):
    txt1 = graphene.Float()
    txt2 = graphene.String()

# Our outer dictionary as an object
class Dictionary(graphene.ObjectType):
    key = graphene.String()
    value = graphene.Field(InnerItem)