from django.db import models

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
    price = models.IntegerField()

    def __str__(self):
        return self.title

