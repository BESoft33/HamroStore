from django.db import models

from store_app.models import Store
from user_app.models import Customer


class Product(models.Model):
    name = models.CharField(max_length=255,)
    image = models.ImageField(upload_to='images', blank=True)
    image_url = models.URLField(blank=True)
    unit_price = models.FloatField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, null=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name
