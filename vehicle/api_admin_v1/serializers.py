from django.http import HttpResponse
from rest_framework import serializers
from ..models import *
from accounts.models import accountsUserModel
from accounts.api_admin_v1.serializers import *
from ..utils import *


# CREATE A VEHICLE
class vehicleCreateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicleMainModel
        fields = '__all__'


# GET ALL VEHICLES
class vehicleGetAllVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicleMainModel
        fields = '__all__'


# BREAKDOWN WITH IMAGE
class vehicleBreakdownWithImageSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField(required=True)
    vehicle_id = serializers.IntegerField(required=True)
    image = serializers.ListField(child=serializers.FileField(allow_null=False, write_only=True, allow_empty_file=False))

    def validate(self, data):
        # print(self, '.......self of validate')
        # print(data, "...............DATA")

        try:
            owner = accountsUserModel.objects.get(id=data.get('owner_id'))
            # print(owner)
        except:
            raise serializers.ValidationError('owner does not exist')
        try:
            vehicle = vehicleMainModel.objects.get(id=data.get('vehicle_id'))
            # print(vehicle)
        except:
            raise serializers.ValidationError('vehicle does not exist')

        vehicle_status = vehicle.status
        if vehicle_status == 'BREAKDOWN':
            raise serializers.ValidationError("Vehicle is already breakdown")
        else:
            pass

        return data

    class Meta:
        model = vehicleBreakdownImageModel
        fields = '__all__'

    def create(self, validated_data):
        # print(self, "..........SELF")
        # print(validated_data, "................VALIDATED DATA")
        owner = validated_data.get('owner_id')
        vehicle = validated_data.get('vehicle_id')
        image = validated_data.get('image', )
        try:
            owner = accountsUserModel.objects.get(id=owner)
            print(owner)
        except:
            raise serializers.ValidationError('owner is not exist with this id')

        try:
            vehicle = vehicleMainModel.objects.get(id=vehicle)
            print(vehicle)
        except:
            raise serializers.ValidationError('vehicle is not exist with this id')

        breakdown = vehicleBreakdownModel.objects.create(owner=owner, vehicle=vehicle, status="BREAKDOWN")
        print(breakdown)
        try:
            if breakdown:
                for img in image:
                    breakdown_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,
                                                                              status='BREAKDOWN')
                vehicle.status = 'BREAKDOWN'
                vehicle.save()

            else:
                raise serializers.ValidationError("breakdown is not updated")
        except Exception as e:
            breakdown.delete()
            raise serializers.ValidationError(f'breakdown is not updated {e}')

        return validated_data


# GET BREAKDOWN DETAILS
class vehicleBreakdownDetails(serializers.ModelSerializer):
    class Meta:
        model = vehicleBreakdownModel
        fields = '__all__'
        read_only_fields = ('id',)


# ASSIGN BREAKDOWN TO USER
class vehicleAssignToUserSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField(required=True)
    breakdown_id = serializers.IntegerField(required=True)

    def validate(self, data):
        # print(self, '.....self of validate in assign')
        # print(data, '.....data of validate in assign')
        try:
            owner = accountsUserModel.objects.get(id=data.get('owner_id'))
            # print(owner)
        except:
            raise serializers.ValidationError('owner does not exist')
        try:
            breakdown = vehicleBreakdownModel.objects.get(id=data.get('breakdown_id'))
            # print(breakdown)
        except:
            raise serializers.ValidationError('vehicle does not exist')
        breakdown_assign = vehicleBreakdownAssignedModel.objects.filter(breakdown=breakdown).last()
        if breakdown_assign:
            raise serializers.ValidationError("this breakdown is already assigned")
        else:
            pass

        return data

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data)

        owner = validated_data.get('owner_id')
        # print(owner)
        breakdown = validated_data.get('breakdown_id')
        # print(breakdown)

        try:
            owner = accountsUserModel.objects.get(id=owner)
            # print(owner)
        except:
            raise serializers.ValidationError('owner is not exist with this id')

        try:
            breakdown = vehicleBreakdownModel.objects.get(id=breakdown)
            # print(breakdown.status, '---------------breakdown status')
        except:
            raise serializers.ValidationError('vehicle is not exist with this id')

        try:
            if breakdown.status == "BREAKDOWN":
                # print(breakdown.status,'------------------break status')
                breakdown_assign = vehicleBreakdownAssignedModel.objects.create(breakdown=breakdown, owner=owner)
                breakdown.status = "ASSIGNED"
                breakdown.save()
                # print(breakdown_status)
            else:
                raise serializers.ValidationError("vehicle status is not in breakdown so we cant proceed")
        except Exception as e:
            raise serializers.ValidationError(f'breakdown is not updated {e}')

        return validated_data


'''INSPECT and REPAIR THE VEHICLE WITH IMAGES'''
class vehicleInspectionWithImageSerializer(serializers.Serializer):
    owner_id = serializers.IntegerField(required=True)
    breakdown_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(max_length=100)
    image = serializers.ListField(child=serializers.FileField(allow_null=False, write_only=True, allow_empty_file=False))
    status = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        try:
            owner = accountsUserModel.objects.get(id=data.get('owner_id'))
        except:
            raise serializers.ValidationError('owner does not exist')
        try:
            breakdown = vehicleBreakdownModel.objects.get(id=data.get('breakdown_id'))
        except:
            raise serializers.ValidationError('breakdown does not exist')

        """user assigned validation """

        assigned = vehicleBreakdownAssignedModel.objects.filter(breakdown=breakdown).last()
        print(owner,'--------------assigned owner')
        if assigned.owner != owner :
            raise serializers.ValidationError('user assigned is not the actual assigned user')

        '''status validation '''

        status = data.get("status")
        last_inspection = vehicleBreakdownInpectionModel.objects.filter(breakdown=breakdown, status=status).last()
        print(last_inspection, "last inspection", status, breakdown)
        if last_inspection:
            raise serializers.ValidationError(f"{status.lower()} already completed")
        # if last_inspection.status and status == 'INSPECTION':
        #     pass
        # else:
        #     if last_inspection.status and status == 'REPAIR':
        #         raise serializers.ValidationError('repair already done')

        return data

    class Meta:
        model = vehicleBreakdownImageModel
        fields = '__all__'

    def create(self, validated_data, **kwargs):
        # print(self, '-----------self validated  of inspection')
        # print(validated_data, '-----validated------data of inspection')
        # print(type(validated_data),'...........type')
        # print(type(self),'...........self type')

        owner = validated_data.get('owner_id')
        breakdown = validated_data.get('breakdown_id')
        reason = validated_data.get('reason')
        image = validated_data.get('image', [])
        status = validated_data.get('status')

        try:
            owner_det = accountsUserModel.objects.get(id=owner)
        except:
            raise serializers.ValidationError('owner does not exist with this id')

        try:
            breakdown = vehicleBreakdownModel.objects.get(id=breakdown)
        except:
            raise serializers.ValidationError('breakdown does not exist with this id')

        try:
            breakdown_inspection_repair = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason,
                                                                                        breakdown=breakdown,
                                                                                        status=status)

            if breakdown_inspection_repair:
                for img in image:
                    inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,
                                                                               status=status)
            if status == "INSPECTION":
                breakdown.status = "INSPECTION"
                breakdown.save()
            elif status == "REPAIR":
                breakdown.status = "COMPLETED"
                breakdown.save()
            else:
                pass
        except:
            pass
        return validated_data


        # if status == "INSPECTION":
        #     try:
        #         inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=breakdown, status="INSPECTION")
        #         if inspection:
        #             for img in image:
        #                 inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img, status='INSPECTION')
        #             breakdown.status = "INSPECTION"
        #             breakdown.save()
        #         else:
        #             raise serializers.ValidationError('images are not updated for inspection')
        #     except Exception as e:
        #         inspection.delete()
        #         raise serializers.ValidationError(f'inspection is not updated due to {e}')
        #
        # elif status == "REPAIR":
        #     try:
        #         repair = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=breakdown, status="REPAIR")
        #         if repair:
        #             for img in image:
        #                 inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img, status='REPAIR')
        #             breakdown.status = "COMPLETED"
        #             breakdown.save()
        #         else:
        #             # repair.delete()
        #             raise serializers.ValidationError('images for repair  are not updated')
        #     except Exception as e:
        #         repair.delete()
        #         raise serializers.ValidationError(f'inspection is not updated due to {e}')

        # return validated_data

        # elif status == "REPAIR":
        #     # Perform repair on the vehicle
        #     try:
        #         repair = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=

        #         pass
        #         # raise serializers.ValidationError('vehicle is not in ASSIGNED status so we cannot proceed further')
        # except Exception as e:
        #     # breakdown.delete()
        #     raise serializers.ValidationError(f"inspection model is not created bcz of {e}")


# repair

# inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=breakdown, status="REPAIR")
# try:
#     if breakdown.status == "INSPECTION":
#         for img in image:
#             inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,
#                                                                        status='REPAIR')
#         breakdown.status = "COMPLETED"
#         breakdown.save()
#         return "Vehicle is IN REPAIR"
#     else:
#         raise serializers.ValidationError('vehicle is not in ASSIGNED status so we cannot proceed further')
# except Exception as e:
#     breakdown.delete()
#     raise serializers.ValidationError(f"inspection model is not created bcz of {e}")


class vehicleGetAllBreakdownDetailsByIdSerializer(serializers.ModelSerializer):
    vehicle = vehicleGetAllVehicleSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        print(self, '........self')
        print(obj, '...............obj')
        try:
            user = accountsGetAllUserDetailsSerializer(obj.owner).data
            print(user, '....user')
        except:
            user = {}
        return user

    class Meta:
        model = vehicleBreakdownModel
        fields = '__all__'

        # inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=breakdown, status ="INSPECTION")
        # print(inspection)
        # try:
        #     if breakdown.status == "ASSIGNED":
        #         inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason,
        #                                                                    breakdown=breakdown,status="INSPECTION")
        #
        #         for img in image:
        #             inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img, status='INSPECTION')
        #         breakdown.status = "INSPECTION"
        #         breakdown.save()
        #         print(breakdown_status)
        #         return "Vehicle is INSPECTION"
        #
        #     else:
        #         raise serializers.ValidationError('vehicle is not in ASSIGNED status so we can not proceed further')
        # except Exception as e:
        #     raise serializers.ValidationError(f'breakdown is not updated {e}')
        # return validated_data

        #
        #
        # #inspection
        # class vehicleInspectionWithImageSerializer(serializers.Serializer):
        #     owner_id = serializers.IntegerField(required=True)
        #     breakdown_id = serializers.IntegerField(required=True)
        #     reason = serializers.CharField(max_length=100)
        #     image = serializers.ListField(
        #         child=serializers.FileField(allow_null=False, write_only=True, allow_empty_file=False))
        #     status = serializers.CharField(max_length=100, required=True)
        #
        #     def validate(self, data):
        #         print(self, '.....self of validate in inspection')
        #         print(data, '.....data of validate in inspection')
        #         try:
        #             owner = accountsUserModel.objects.get(id=data.get('owner_id'))
        #             print(owner)
        #         except:
        #             raise serializers.ValidationError('owner does not exist')
        #         try:
        #             breakdown = vehicleBreakdownModel.objects.get(id=data.get('breakdown_id'))
        #             print(breakdown)
        #         except:
        #             raise serializers.ValidationError('breakdown does not exist')
        #         """inspection or repair"""
        #         status = data.get("status")
        #         breakdown_inspect = vehicleBreakdownInpectionModel.objects.filter(breakdown=breakdown).last()
        #         if breakdown_inspect:
        #             if status == "INSPECTION":
        #                 if breakdown_inspect.status == "INSPECTION":
        #                     raise serializers.ValidationError("Inspection already completed")
        #             elif status == "REPAIR":
        #                 if breakdown_inspect.status != "INSPECTION":
        #                     raise serializers.ValidationError("Cannot perform repair without inspection")
        #             else:
        #                 pass
        #         else:
        #             pass
        #             return data
        #
        #         # status = data.get("status")
        #         # breakdown_inspect = vehicleBreakdownModel.objects.filter(status=status).last()
        #         # if breakdown_inspect:
        #         #     raise serializers.ValidationError(f"{status.lower()} already completed")
        #         # else:
        #         #     pass
        #
        #     class Meta:
        #         model = vehicleBreakdownImageModel
        #         fields = '__all__'
        #
        #     def create(self, validated_data, **kwargs):
        #         print(self, '.....self of validated data in inspection')
        #         print(validated_data, '.....data of validated_data in inspection')
        #
        #         owner = validated_data.get('owner_id')
        #         print(owner)
        #         breakdown = validated_data.get('breakdown_id')
        #         reason = validated_data.get('reason')
        #         image = validated_data.get('image', [])
        #         status = validated_data.get('status')
        #         print(status, '--------status')
        #
        #         try:
        #             owner_det = accountsUserModel.objects.get(id=owner)
        #             print(owner)
        #         except:
        #             raise serializers.ValidationError('owner is not exist with this id')
        #
        #         try:
        #             breakdown = vehicleBreakdownModel.objects.get(id=breakdown)
        #             print(breakdown)
        #         except:
        #             raise serializers.ValidationError('breakdown is not exist with this id')
        #
        #         if status == "ASSIGNED":
        #
        #             # if breakdown.status == "ASSIGNED":
        #             try:
        #                 inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason,
        #                                                                            breakdown=breakdown,
        #                                                                            status="INSPECTION")
        #                 for img in image:
        #                     inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,
        #                                                                                status='INSPECTION')
        #                 breakdown.status = "INSPECTION"
        #                 breakdown.save()
        #                 return "Vehicle is INSPECTION"
        #             except Exception as e:
        #                 raise serializers.ValidationError(f'inspection is not updated due to {e}')
        #             # else:
        #             #     raise serializers.ValidationError('vehicle is not in ASSIGNED status so we cannot proceed further')
        #
        #         elif status == "INSPECTION":
        #             # if breakdown.status == "INSPECTION":
        #             try:
        #                 repair = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason,
        #                                                                        breakdown=breakdown, status="REPAIR")
        #                 for img in image:
        #                     repair_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,
        #                                                                            status='REPAIR')
        #
        #                 breakdown.status = "REPAIR"
        #                 breakdown.save()
        #                 return "Vehicle is REPAIR"
        #             except Exception as e:
        #                 raise serializers.ValidationError(f'repair is not updated bcz of {e}')
        #             # else:
        #             #     raise serializers.ValidationError(
        #             #         'vehicle is not in INSPECTION status so we cannot proceed further')
        #
        #         else:
        #             raise serializers.ValidationError('invalid status')

# REPAIR WITH IMAGE:
# class vehicleRepairWithImageSerializer(serializers.Serializer):
#     owner_id = serializers.IntegerField(required=True)
#     breakdown_id = serializers.IntegerField(required=True)
#     reason = serializers.CharField(required=True)
#     image = serializers.ListField(child=serializers.FileField(allow_null=False, write_only=True, allow_empty_file=False))
#
#     def validate(self, data):
#         print(self, '.....self of validate in repair')
#         print(data, '.....data of validate in repair')
#         try:
#             owner = accountsUserModel.objects.get(id=data.get('owner_id'))
#             print(owner)
#         except:
#             raise serializers.ValidationError("owner doesn't exist")
#         try:
#             breakdown = vehicleBreakdownModel.objects.get(id=data.get('breakdown_id'))
#             print(breakdown)
#         except:
#             raise serializers.ValidationError("breakdown doesn't  exist")
#
#
#         breakdown_repair = vehicleBreakdownInpectionModel.objects.filter(breakdown=breakdown).last()
#         if breakdown_repair and breakdown_repair.status == "REPAIR":
#             raise serializers.ValidationError("This breakdown has already been repaired")
#         else:
#             pass
#
#         print(data, '.................data')
#         return data
#
#
#     class Meta:
#         model = vehicleBreakdownModel
#         fields = '__all__'
#
#     def create(self, validated_data):
#         print(self, '.....self of validated data in repair')
#         print(validated_data, '.....data of validated data in repairsss')
#
#         owner = validated_data.get('owner_id')
#         print(owner)
#         breakdown = validated_data.get('breakdown_id')
#         reason = validated_data.get('reason')
#         image = validated_data.get('image',[])
#         print(owner, breakdown, reason, image)
#
#
#         try:
#             owner_det = accountsUserModel.objects.get(id=owner)
#             print(owner)
#         except:
#             raise serializers.ValidationError("owner is doesn't exist with this id")
#
#         try:
#             breakdown = vehicleBreakdownModel.objects.get(id=breakdown)
#             print(breakdown)
#         except:
#             raise serializers.ValidationError("'breakdown is  doesn't exist with this id'")
#
#         # inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason, breakdown=breakdown, status ="REPAIR")
#         # print(inspection)
#         try:
#             if breakdown.status == "INSPECTION":
#                 inspection = vehicleBreakdownInpectionModel.objects.create(owner=owner_det, reason=reason,
#                                                                            breakdown=breakdown, status="REPAIR")
#
#                 for img in image:
#                     inspection_img = vehicleBreakdownImageModel.objects.create(breakdown=breakdown, image=img,  status="REPAIR")
#                 breakdown.status = "COMPLETED"
#                 breakdown.save()
#
#                 return "Vehicle is INSPECTION"
#
#             else:
#                 raise serializers.ValidationError('breakdown status is not in inspection, we cant proceed')
#         except Exception as e:
#             raise serializers.ValidationError(f"breakdown is not updated {e}")
#
#         return validated_data


# GET BREAKDOWN HISTORY:
# class vehicleGetAllImageSerializer(serializers.ModelSerializer):
#     class Meta:
# #         model = vehicleBreakdownImageModel
# #         fields = '__all__'
# image = vehicleGetAllImageSerializer(read_only=True, many=True)
# class vehicleGetAllBreakdownDetailsByIdSerializer(serializers.ModelSerializer):
#     vehicle = vehicleGetAllVehicleSerializer(read_only=True)
#     user = serializers.SerializerMethodField()
#
#     def get_user(self, obj):
#         print(self, '........self')
#         print(obj,'...............obj')
#         try:
#             user = accountsGetAllUserDetailsSerializer(obj.owner).data
#             print(user,'....user')
#         except:
#             user = {}
#         return user
#
#     class Meta:
#         model = vehicleBreakdownModel
#         fields = '__all__'
