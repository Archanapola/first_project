from rest_framework import serializers

from accounts.api_admin_v1.serializers import accountsGetAllUserDetailsSerializer
from accounts.models import *
from ..models import *
class orderCreateOrderSerializer(serializers.Serializer):

    def validate(self, data):

        owner = self.context['request'].user

        if not owner.is_authenticated:
            raise serializers.ValidationError('User is not authenticated')

        try:
            cart = accountsUserCartModel.objects.get(owner=owner)
        except:
            raise serializers.ValidationError(' this user cart is empty')



        return data

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context['request'].user
        price = validated_data.get('price')
        final_price = validated_data.get('final_price')

        cart = accountsUserCartModel.objects.get(owner=owner)

        try:
            order = orderMainModel.objects.get(owner=owner, final_price=cart.price, status ='PENDING')
        except:
            order = orderMainModel.objects.create(owner=owner, final_price=cart.price, status = 'PENDING')

        order.products.add(*cart.products.all())
        user_products_all=cart.products.all()
        for item in user_products_all:
            cart_product = accountsUserCartProductModel.objects.filter(owner=owner, product_status='CART',product=item.product).update(
                status="COMPLETED"
            )
        order.save()

        cart.delete()
        return validated_data

class orderGetAllOrdersDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = orderMainModel
        fields = '__all__'










class orderUpdateStatusSerializer(serializers.ModelSerializer):
    # status = serializers.ChoiceField(choices=['PENDING','PROCESSING','OUT FOR DELIVERY','COMPLETED','CANCELLED'], required=True)
    # order_id = serializers.IntegerField(read_only=True)
    def validate(self, data):
        # print(data)
        updated_status = data.get('status')
        owner = self.context['request'].user
        order_id = self.context['order_id']
        owner_order = orderMainModel.objects.filter(id=order_id, owner__id=owner.id)
        print(order_id,'-------order')
        if not owner_order.exists():
            raise serializers.ValidationError({'message':"owner is not same for this order id"})


        if updated_status not in ["PENDING", "PROCESSING","OUT FOR DELIVERY","COMPLETED","CANCELLED"]:
            raise serializers.ValidationError('status is invalid')
        if updated_status == self.instance.status:
            raise serializers.ValidationError('status is already in same status ')
        if updated_status == "PENDING":
            raise serializers.ValidationError('you cant update status as pending ')

        if updated_status == "PROCESSING" and self.instance.status != "PENDING":
            raise serializers.ValidationError('you cant update status to processing')
        if updated_status == 'CANCELLED' and self.instance.status not in ['PENDING', 'PROCESSING']:
            raise serializers.ValidationError('you cant update status to canclled')
        if updated_status == 'OUT FOR DELIVERY' and self.instance.status != 'PROCESSING':
            raise serializers.ValidationError('you cant update status to out for delivery')
        if updated_status == 'COMPLETED' and self.instance.status != 'OUT FOR DELIVERY':
            raise serializers.ValidationError('you cant update status to completed')
        return data

    class Meta:
        model = orderMainModel
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        return instance


class orderGetOrdersByUserIdSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()


    def get_owner(self, obj):
        print(obj, 'obj')

        print(obj.owner)
        owner = accountsGetAllUserDetailsSerializer(obj.owner).data
        return owner
    # def validate(self, data):
    #     owner = data.get('owner')
    #     try:
    #         owner_det = accountsUserModel.objects.get(id=owner.id)
    #     except:
    #         raise serializers.ValidationError('user not exist')
    class Meta:
        model = orderMainModel
        fields ='__all__'










