from django.db import models
#
# from .models import accountsUserModel,accountsUserCartProductModel
from accounts.models import accountsUserModel, accountsUserCartProductModel
from django.db.models.signals import post_save
#
# def create_profiles(sender, instance, created, **kwargs):
#     if created:
#         try:
#             wishlist = wishlistMainModel.objects.create(owner=instance)
#             wishlist.save()
#             print(wishlist, '..created...')
#         except Exception as e:
#             print('Error creating wishlist:', str(e))

class wishlistMainModel(models.Model):
    owner = models.OneToOneField(accountsUserModel, on_delete=models.CASCADE, related_name='wishlistMainModel_owner')
    products = models.ManyToManyField(accountsUserCartProductModel, related_name='wishlistMainModel_products')


# post_save.connect(create_profiles, sender=accountsUserModel)
