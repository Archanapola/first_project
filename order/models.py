from django.db import models
from accounts.models import *
# Create your models here.

ORDER_STATUS=(
    ('PENDING', 'PENDING'),
    ('PROCESSING', 'PROCESSING'),
    ('OUT FOR DELIVERY', 'OUT FOR DELIVERY'),
    ('COMPLETED', 'COMPLETED'),
    ('CANCELLED', 'CANCELLED'),
)

class orderMainModel(models.Model):
    owner = models.ForeignKey(accountsUserModel, on_delete=models.CASCADE, related_name='orderMainModel_owner')
    products = models.ManyToManyField(accountsUserCartProductModel, related_name='orderMainModel_products')
    final_price = models.DecimalField(max_digits=10, default=0,decimal_places=2)
    status = models.CharField(max_length=40, choices=ORDER_STATUS)