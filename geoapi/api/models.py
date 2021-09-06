from django.db import models

class IpGeolocationData(models.Model):
    ip = models.GenericIPAddressField()
    continent_name = models.CharField(max_length=50)
    country_name = models.CharField(max_length=100)
    region_name = models.CharField(max_length=400)
    city = models.CharField(max_length=400)
    zip_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)