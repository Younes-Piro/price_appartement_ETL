import graphene
from .models import Appartement
from .mutation import AppartementsType

# query are useful to query the data from our database

class Query(graphene.ObjectType):

    all_appartements = graphene.List(AppartementsType)
    single_appartement = graphene.Field(AppartementsType, id=graphene.Int()) #getting a single book my id

    def resolve_all_appartements(root, info):
        return Appartement.objects.all()
        
    def resolve_single_appartement(root, info, id):
        return Appartement.objects.get(pk=id)
    
# importing the schema
schema = graphene.Schema(query=Query)