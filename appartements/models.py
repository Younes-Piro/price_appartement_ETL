from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Sum

class Appartement(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    security = models.IntegerField()
    garage = models.IntegerField()
    concierge = models.IntegerField()
    city = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    nmbr_of_rooms = models.IntegerField()
    Nmbr_of_pieces = models.IntegerField()
    Nmbr_of_bathrooms = models.IntegerField()
    type = models.CharField(max_length=100)
    surface = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.title


class AuthorManager(models.Manager):
    def get_queryset(self):
        return AuthorQuerySet(self.model, using=self._db)

    def annotate_with_copies_sold(self):
        return self.get_queryset().annotate_with_copies_sold()


class AuthorQuerySet(models.QuerySet):
    def annotate_with_copies_sold(self):
        return self.annotate(copies_sold=Sum('price'))







