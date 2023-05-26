from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.manage import CustomUserManager
from product.models import productMainModel


# from wishlist.models import wishlistMainModel


# Create your models here.
#
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = accountsUserProfileModel.objects.create(owner=instance)
#         user_profile.save()
#         print(user_profile,'..created...')
#     if not created:
#         print(instance, '..not created...')
# def create_profiles(sender, instance, created, **kwargs):
#     if created:
#         try:
#             user_profile = accountsUserProfileModel.objects.create(owner=instance)
#             user_profile.save()
#             print(user_profile, '..created...')
#         except Exception as e:
#             print('Error creating user profile:', str(e))
#
#         try:
#             user_cart = accountsUserCartModel.objects.create(owner=instance)
#             user_cart.save()
#             print(user_cart, '..created...')
#         except Exception as e:
#             print('Error creating user cart:', str(e))
#     else:
#         print(instance, '..not created...')


class accountsUserModel(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique=True)
    phone_number = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=False, unique=True)
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        # return self.phone_number
        return str(self.email) + " --- " + str(self.id)


# post_save.connect(create_profiles, sender=accountsUserModel)

GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHERS', 'OTHERS'),
)


class accountsUserProfileModel(models.Model):
    owner = models.OneToOneField(accountsUserModel, on_delete=models.CASCADE,
                                 related_name='accountsUserProfileModel_owner')
    name = models.CharField(max_length=30, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        # return self.phone_number
        return str(self.owner)


def deactivate_previous_otp(sender, instance, created, **kwargs):
    if created:
        all_otp = accountsUserLoginOtpModel.objects.filter(owner=instance.owner)
        if len(all_otp) > 1:
            previous_otp = all_otp.order_by('-id')[1]
            previous_otp.active = False
            previous_otp.save()


class accountsUserLoginOtpModel(models.Model):
    owner = models.ForeignKey(accountsUserModel, null=True, on_delete=models.CASCADE,
                              related_name='accountsUserLoginOtpModel_owner')
    otp = models.IntegerField()
    active = models.BooleanField(default=True)


post_save.connect(deactivate_previous_otp, sender=accountsUserLoginOtpModel)

PRODUCT_STATUS = (
    ('CART', 'CART'),
    ('WISHLIST', 'WISHLIST'),
)

STATUS = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
)


class accountsUserCartProductModel(models.Model):
    owner = models.ForeignKey(accountsUserModel, null=True, on_delete=models.CASCADE,
                              related_name='accountsUserCartProductModel_owner')
    product = models.ForeignKey(productMainModel, null=True, on_delete=models.CASCADE,
                                related_name='accountsUserCartProductModel_product')
    product_status = models.CharField(max_length=30, choices=PRODUCT_STATUS)
    status = models.CharField(max_length=30, choices=STATUS)

    # def __str__(self):
    #     # return self.phone_number
    #     return str(self.product)+'-----'+str(self.id)

class accountsUserCartModel(models.Model):
    owner = models.OneToOneField(accountsUserModel, null=True, on_delete=models.CASCADE,
                                 related_name='accountsUserCartModel_owner')
    products = models.ManyToManyField(accountsUserCartProductModel, related_name='accountsUserCartModel_products')
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)

