from django.db import models
from .utils import *
# from first_project_core.accounts.models import accountsUserModel
from accounts.models import *

from accounts.models import accountsUserModel


# from accounts.models import *
# Create your models


class vehicleMainModel(models.Model):
    title = models.CharField(max_length=30)
    vehicle_no = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=vehicle_status.choices())
    image = models.ImageField()

    def __str__(self):
        # return self.id
        return str(self.title) + " --- " + str(self.id)


class vehicleBreakdownModel(models.Model):
    # objects = None
    owner = models.ForeignKey(accountsUserModel, on_delete=models.CASCADE, related_name='vehicleBreakdownModel_owner')
    vehicle = models.ForeignKey(vehicleMainModel, on_delete=models.CASCADE, related_name='vehicleBreakdownModel_vehicle')
    status = models.CharField(max_length=20, choices=breakdown_status.choices())

    # def __str__(self):
    #     # return self.id
    #     return str(self.owner)+ '-'+str(self.id)

class vehicleBreakdownImageModel(models.Model):
    breakdown = models.ForeignKey(vehicleBreakdownModel, on_delete=models.CASCADE, related_name='vehicleBreakdownImageModel_breakdown')
    image = models.ImageField()
    status = models.CharField(max_length=20, choices=image_status.choices())

    def __str__(self):
        # return self.id
        return str(self.breakdown.owner) + " --- " + str(self.id)

class vehicleBreakdownAssignedModel(models.Model):

    breakdown = models.OneToOneField(vehicleBreakdownModel, on_delete=models.CASCADE, related_name='vehicleBreakdownAssignedModel_breakdown')
    owner = models.ForeignKey(accountsUserModel, on_delete=models.CASCADE, related_name='vehicleBreakdownAssignedModel_owner')


class vehicleBreakdownInpectionModel(models.Model):
    breakdown = models.ForeignKey(vehicleBreakdownModel, on_delete=models.CASCADE, related_name='vehicleBreakdownInpectionModel_breakdown')
    owner = models.ForeignKey(accountsUserModel, on_delete=models.CASCADE, related_name='vehicleBreakdownInpectionModel_owner')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=inspection_status.choices())

    def __str__(self):
        # return self.id
        return str(self.status)


