from django.db import models
from user_app.models import BaseUser

class Store(models.Model):
    store_name      = models.CharField(max_length=200)
    location        = models.CharField(max_length=200, null=True)
    phone           = models.CharField(max_length=10, unique=True)
    register_date   = models.DateField(auto_now_add=True)
    last_modified_on= models.DateField(auto_now=True)
    is_verified     = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = 'store'

class StoreAdmin(models.Model):
    store = models.OneToOneField(Store,on_delete=models.CASCADE, related_name='store')
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='admin')
    role    = BaseUser.STORE_ADMIN
    
    class Meta:
        verbose_name = 'Admin'
        db_table     = 'store_admin'

    def __str__(self):
        return f"{self.store}"






