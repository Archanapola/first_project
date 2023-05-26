from rest_framework import serializers
from ..models import *
from wishlist.models import *
from accounts.models import *
# create user
class productCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = productMainModel
        fields = '__all__'

class productImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productImageModel
        fields = '__all__'


class productGetProductsWithImagesSerializer(serializers.ModelSerializer):
    product_image = productImageSerializer(read_only=True,many=True, source='productImageModel_product')
    class Meta:
        model = productMainModel
        fields = '__all__'


class productCreateProductWithMultipleImagesSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50, write_only=True)
    description = serializers.CharField(max_length=200, write_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    image = serializers.ListField(child=serializers.FileField(allow_null=False, write_only=True,required=True, allow_empty_file=False))
    def validate(self, data):

        product = productMainModel.objects.filter(title=data.get('title'), description = data.get('description'), price=data.get('price'))
        print(product)
        if product.exists():
            raise serializers.ValidationError('product already exists')

        return data

    class Meta:
        model = productImageModel
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        price = validated_data.get('price')
        image = validated_data.get('image',[] )

        product = productMainModel.objects.create(title= title, description=description,price=price)
        print(product)
        try:
            if product:
                for img in image:
                    product_image = productImageModel.objects.create(product=product, image=img)
                product.save()

            else:
                raise serializers.ValidationError("product images  not updated")
        except Exception as e:
            product.delete()
            raise serializers.ValidationError(f'images are  not updated {e}')

        return validated_data


class productAddProductToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)

    def validate(self, data):

        owner = self.context['request'].user
        if not owner.is_authenticated:
            raise serializers.ValidationError('User is not authenticated')
        product_id = data.get('product_id')
        try:
            product = productMainModel.objects.get(id=product_id)
        except:
            raise serializers.ValidationError('Product does not exist')

        product = accountsUserCartProductModel.objects.filter(product=product, owner=owner, status='PENDING', product_status='CART')

        if product.exists():
            raise serializers.ValidationError('product already exist')


        return data

    def create(self, validated_data):
        owner = self.context['request'].user

        product_id = validated_data.get('product_id')
        product = productMainModel.objects.get(id=product_id)

        try:
           product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='CART', status='PENDING')
        except:
            raise serializers.ValidationError('Product already exists in cart')
        try:
            cart = accountsUserCartModel.objects.get(owner=owner)
        except:
            cart = accountsUserCartModel.objects.create(owner=owner)



        cart.products.add(product_cart.id)
        total_price = 0
        products_all = cart.products.all()
        for item in products_all:
            total_price += int(item.product.price)
        cart.price = total_price
        cart.save()
        return validated_data

class productGetAllUserCartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountsUserCartModel
        fields = '__all__'

#get user cart by passing-id:

class productGetUserCartProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = accountsUserCartProductModel
        fields = '__all__'

        # fields = ('id', 'product', 'product_status', 'status')

class productGetUserCartByIdSerializer(serializers.ModelSerializer):
    products = productGetUserCartProductsSerializer(many=True)
    # print(products,'------------------productdetiasls')

    class Meta:
        model = accountsUserCartModel
        # fields = ('id', 'owner', 'products', 'price')
        fields = '__all__'













# class productAddProductToWishlistSerializer(serializers.Serializer):
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
#
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
#         except wishlistMainModel.DoesNotExist:
#             wishlist = wishlistMainModel.objects.create(owner=owner)
#
#         if wishlist.products.filter(id=product.id).exists():
#             wishlist.products.remove(product)
#             raise serializers.ValidationError('product is removed from wishlist')
#         else:
#             wishlist.products.add(product)
#             raise serializers.ValidationError('product is added to wishlist')
#
#         return  validated_data
#

        # try:
        #     product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product,
        #                                                                product_status='WISHLIST', status='PENDING')
        #     print(product_cart,'-product cart')
        # except:
        #     raise serializers.ValidationError('Product already exists in cart')
        # try:
        #     wishlist = wishlistMainModel.objects.get(owner=owner)
        #     print(wishlist,'--------wihslist')
        # except:
        #     wishlist = wishlistMainModel.objects.create(owner=owner)
        #     print(wishlist,'-wihslist')

            # wishlist.products.add(product_cart.id)
            # wishlist.products.add(product_cart.id)

        # try:
        #     wishlist = wishlistMainModel.objects.get(owner=owner)
        #     product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
        #     if wishlist.products.filter(id=product_cart.id).exists():
        #         wishlist.products.remove(product_cart)
        #         raise serializers.ValidationError('product is removed from to wishlist')
        #
        #     else:
        #         wishlist.products.add(product_cart)
        #         raise serializers.ValidationError('product is added to wishlist')
        # except Exception as e:
        #     # wishlist = wishlistMainModel.objects.create(owner=owner)
        #     # product_cart = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
        #     # wishlist.products.add(product_cart)
        #     raise serializers.ValidationError(f'product is added to wishlist')




























        # product = validated_data.get('product')
        #
        # product_main = productMainModel.objects.get(product=product)
        # try:
        #    product = accountsUserCartProductModel.objects.create(owner=owner, product=product, product_status='WISHLIST', status='PENDING')
        # except:
        #     raise serializers.ValidationError('Product already exists in cart')
        # try:
        #     product_wishlist = wishlistMainModel.objects.get(owner=owner)
        # except:
        #     product_wishlist = wishlistMainModel.objects.create(owner=owner)
        #
        # product_wishlist.products.add(product.id)
        #
        # return validated_data



