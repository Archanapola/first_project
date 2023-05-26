from accounts.models import accountsUserCartProductModel, accountsUserModel, accountsUserCartModel
from product.models import productMainModel
from wishlist.models import wishlistMainModel
from rest_framework import serializers

#
class wishlistAddProductToWishlistSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)

    def validate(self, data):
        owner = self.context['request'].user
        if not owner.is_authenticated:
            raise serializers.ValidationError('User is not authenticated')
        product_id = data.get('product_id')
        try:
            product = productMainModel.objects.get(id=product_id)
            print(product,'--------product')
        except:
            raise serializers.ValidationError('Product does not exist')

        # product = accountsUserCartProductModel.objects.filter(product=product,product_status='WISHLIST', owner=owner)
        #
        # if product.exists():
        #     product.delete()
        #     pass
            # raise serializers.ValidationError('product already exist')
        return data

    def create(self, validated_data):
        owner = self.context['request'].user
        # print(owner,'-----------owner')
        product_id = validated_data.get('product_id')
        # print(product_id,'--------product_id')
        product = productMainModel.objects.get(id=product_id)
        # print(product,'-----------product')
        instance_owner=accountsUserModel.objects.get(id=owner.id)

        try:
           product_cart = accountsUserCartProductModel.objects.get(owner=instance_owner, product=product, product_status='WISHLIST', status='PENDING')
           print(product_cart,'-----------------------------cart')
        except:
            product_cart = accountsUserCartProductModel.objects.create(owner=instance_owner, product=product,
                                                                       product_status='WISHLIST', status='PENDING')
        try:
            wishlist = wishlistMainModel.objects.get(owner=instance_owner)
        except:
            wishlist = wishlistMainModel.objects.create(owner=instance_owner)

        all_wish_list_products=wishlist.products.all()
        if product_cart not in all_wish_list_products:
            wishlist.products.add(product_cart.id)
            wishlist.save()
            raise serializers.ValidationError({'message':'product added to wishlist'})

        if product_cart in all_wish_list_products:
            wishlist.products.remove(product_cart.id)
            wishlist.save()
            raise serializers.ValidationError({'message':'product removed from wishlist'})


        return validated_data



class wishlistGetAllwishlistDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = wishlistMainModel
        fields = '__all__'

#get user cart by passing-id:

class wishlistGetUserWishlistProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = accountsUserCartProductModel
        fields = '__all__'

        # fields = ('id', 'product', 'product_status', 'status')

class wishlistGetUserWishlistByIdSerializer(serializers.ModelSerializer):
    products = wishlistGetUserWishlistProductsSerializer(many=True)
    # print(products,'------------------productdetiasls')

    class Meta:
        model = wishlistMainModel
        # fields = ('id', 'owner', 'products', 'price')
        fields = '__all__'






























#     product_id = serializers.IntegerField(required=True)
#
#     def validate(self, data):
#         product_id = data.get('product_id')
#
#         owner = self.context['request'].user
#         print(owner,'------owner')
#         if not owner.is_authenticated:
#             raise serializers.ValidationError('User is not authenticated')
#         product_id = data.get('product_id')
#         try:
#             product = productMainModel.objects.get(id=product_id)
#             print(product,'-------product')
#         except:
#             raise serializers.ValidationError('product is not exist')
#         product_cart = accountsUserCartProductModel.objects.filter(owner=owner, product=product,
#                                                                    product_status='WISHLIST', status='PENDING')
#         if product_cart.exists():
#             product_cart.delete()
#             pass
#             # raise serializers.ValidationError('product already exist')
#
#         try:
#             product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product,
#                                                                        product_status='WISHLIST', status='PENDING')
#             print(product_cart, '----------product cart created')
#         except Exception as e:
#             raise serializers.ValidationError(f"product not created{e}")
#
#         return data
#
#     class Meta:
#         fields = '__all__'
#
#     def create(self, validated_data):
#         owner = self.context['request'].user
#         print(owner, '--owner')
#
#         product_id = validated_data.get('product_id')
#
#         product = productMainModel.objects.get(id=product_id)
#         print(product,'---product')
#         try:
#             wishlist = wishlistMainModel.objects.get(owner=owner)
#
#         except:
#             wishlist = wishlistMainModel.objects.create(owner=owner)
#
#         try:
#             if wishlist.products.filter(id=product.id).exists():
#                 wishlist.products.remove(product)
#                 raise serializers.ValidationError('product is removed from wishlist')
#             else:
#                 wishlist.products.add(product)
#                 # try:
#                 #     product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
#                 #     print(product_cart,'----------product cart created')
#                 #     product_cart.save()
#                 #     return product_cart
#                 # except Exception as e:
#                 #     raise serializers.ValidationError(f"product not created{e}")
#
#         except Exception as e:
#             raise serializers.ValidationError(f'Product is not created in product cart model {e}')
#         return validated_data
#
#
#         # try:
#         #     product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
#         # except Exception as e:
#         # raise serializers.ValidationError(f'Product is not created in product cart model {e}')
#
#         # try:
#         #     product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
#         # except:
#         #     raise serializers.ValidationError('Product already exists in cart')
#         #
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# #
# # class productAddProductToWishlistSerializer(serializers.Serializer):
# #     product_id = serializers.IntegerField(required=True, write_only=True)
# #     product_st = serializers.CharField(read_only=True)
# #
# #     def validate(self, data):
# #         owner = self.context['request'].user
# #         if not owner.is_authenticated:
# #             raise serializers.ValidationError('User is not authenticated')
# #         product_id = data.get('product_id')
# #
# #         try:
# #             product = productMainModel.objects.get(id=product_id)
# #         except :
# #             raise serializers.ValidationError('Product does not exist')
# #
# #         return data
# #
# #     class Meta:
# #         fields = '__all__'
# #
# #     def create(self, validated_data):
# #         owner = self.context['request'].user
# #         product_id = validated_data.get('product_id')
# #         product = productMainModel.objects.get(id=product_id)
# #         owner_instance=accountsUserModel.objects.get(id=owner.id)
# #
# #         try:
# #             wishlist = wishlistMainModel.objects.get(owner=owner_instance)
# #             # if product in wishlist.products.all():
# #             #     wishlist.products.remove(product)
# #             product_st = 'Product removed from wishlist'
# #                 # accountsUserCartProductModel.objects.get(owner=owner, product=product, product_status='WISHLIST').delete()
# #         #     # else:
# #         #     #     wishlist.products.add(product)
# #         #     product_st = 'Product to remove wishlist'
# #         #     #     accountsUserCartProductModel.objects.create(owner=owner,product=product, product_status='WISHLIST',status='PENDING')
# #         except:
# #             wishlist = wishlistMainModel.objects.create(owner=owner_instance)
# #         #     wishlist.products.add(product)
# #             product_st = 'Product added to wishlist'
# #         #     accountsUserCartProductModel.objects.create(
# #         #         owner=owner,
# #         #         product=product,
# #         #         product_status='WISHLIST',
# #         #         status='PENDING'
# #         #     )
# #         #
# #         validated_data['product_st'] = product_st
# #         return validated_data
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# #
# # class productAddProductToWishlistSerializer(serializers.Serializer):
# #     product_id = serializers.IntegerField(required=True,write_only=True)
# #     product_st =serializers.CharField(read_only=True)
# #
# #     def validate(self, data):
# #         owner = self.context['request'].user
# #         print(owner, '------owner')
# #         if not owner.is_authenticated:
# #             raise serializers.ValidationError('User is not authenticated')
# #         product_id = data.get('product_id')
# #
# #         try:
# #             product = productMainModel.objects.get(id=product_id)
# #             print(product,'-------product')
# #         except:
# #             raise serializers.ValidationError('product is not exist')
# #         # product_cart = accountsUserCartProductModel.objects.filter(product=product, product_status='WISHLIST', owner=owner)
# #         #
# #         # if product_cart.exists():
# #         #     raise serializers.ValidationError('product already exist')
# #
# #         return data
# #
# #
# #     class Meta:
# #         fields = '__all__'
# #
# #     def create(self, validated_data):
# #         owner = self.context['request'].user
# #         print(owner, '--owner')
# #
# #         product_id = validated_data.get('product_id')
# #
# #         product = productMainModel.objects.get(id=product_id)
# #         print(product,'---product')
# #
# #         if product:
# #             product_st="product added to wishlist"
# #         else:
# #             product_st="product remove to wishlist"
# #
# #         validated_data['product_st']=product_st
# #         return  validated_data
# #
# #         try:
# #            product_cart = accountsUserCartProductModel.objects.get(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
# #            print(product_cart,'--------product_cart')
# #         except:
# #             product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product,product_status='WISHLIST', status='PENDING')
# #
# #         #     print(product_cart,'----------------new created')
# #
# #         try:
# #             wishlist = wishlistMainModel.objects.get(owner=owner)
# #             wishlist.products.remove(product.id)
# #             wishlist.save()
# #             product_cart.delete()
# #             print("prodct is removed from wishlist")
# #             # raise serializers.ValidationError('product is added to wishlist')
# #
# #
# #         except :
# #             wishlist = wishlistMainModel.objects.create(owner=owner)
# #             wishlist.products.add(product.id)
# #             wishlist.save()
# #             print("prodct is added to wishlist")
#         #
#             # raise serializers.ValidationError('product is removed from wishlist')
#         # return  validated_data
#
#
#
#         # if wishlist.products.filter(id=product.id).exists():
#         #     wishlist.products.remove(product)
#         #     raise serializers.ValidationError('product is removed from wishlist')
#         # else:
#         #     wishlist.products.add(product)
#         #     raise serializers.ValidationError('product is added to wishlist')
#
#
