from django.urls import path

from .ETL.transform import clean
from .ETL.extract import scrap
from .ETL.load import load

urlpatterns = [
    #path('', scrap)
    #path('',clean)
    #path('',load)

]