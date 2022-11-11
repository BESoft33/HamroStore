from django.db import models
from django.contrib.auth.models import User


class BaseUser(models.Model):
    
    STORE_ADMIN         = 1 
    CUSTOMER            = 2
    PROJECT_ADMIN       = 3

    ROLE_CHOICES = (
        (STORE_ADMIN,'Store Manager'),
        (CUSTOMER, 'Customer'),
        (PROJECT_ADMIN,'Project Admin')
    )

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='base_user', related_query_name='base_user')
    role            = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CUSTOMER)


    
class Customer(models.Model):
    user:BaseUser = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer')

    class Meta:
        db_table        = 'customers'
        verbose_name    = 'Customer'
        





