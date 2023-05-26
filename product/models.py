import random

from django.db import models
from django.db.models.signals import pre_save


# Create your models here.

def generate_unique_id(sender, instance, **kwargs):
    if not instance.unique_id:
        instance.unique_id = random.randint(100000, 999999)
        while sender.objects.filter(unique_id=instance.unique_id).exists():
            instance.unique_id = random.randint(100000, 999999)


class productMainModel(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    unique_id = models.IntegerField(unique=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # return self.phone_number
        return str(self.title) + " --- " + str(self.id)

pre_save.connect(generate_unique_id, sender=productMainModel)

class productImageModel(models.Model):
    product = models.ForeignKey(productMainModel, on_delete=models.CASCADE, related_name='productImageModel_product')
    image = models.ImageField()