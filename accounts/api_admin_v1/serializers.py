import random
from random import randint
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from wishlist.models import wishlistMainModel
from django.core.mail import send_mail
from rest_framework import serializers

from first_project_core import settings
from ..models import *
# from rest_framework_simplejwt.tokens import
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# create user
class accountsUserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)
    phone_number = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=['MALE', 'FEMALE', 'OTHERS'], write_only=True)
    image = serializers.ImageField()

    def validate(self, data):

        # try:
        owner = accountsUserModel.objects.filter(email=data.get('email'), phone_number=data.get('phone_number'))
        if owner.exists():
            raise serializers.ValidationError('user already exist')

        return data
    class Meta:
        model = accountsUserModel
        fields = '__all__'

    def create(self, validated_data):
        # owner =validated_data.get('owner')
        name = validated_data.get('name')
        dob = validated_data.get('dob')
        image = validated_data.get('image')
        gender = validated_data.get('gender')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        try:
            owner = accountsUserModel.objects.create(email=email, phone_number=phone_number)
        except Exception as e:
            raise serializers.ValidationError(f"user model is not created  {e}")
        try:
            user_profile = accountsUserProfileModel.objects.create(owner=owner, name=name, dob=dob, gender=gender,
                                                                   image=image)
        except Exception as e:
            raise serializers.ValidationError(f"user profile model is not created  {e}")

        try:
            user_cart = accountsUserCartModel.objects.create(owner = owner)
        except Exception as e:
            raise serializers.ValidationError(f"user cart model is not created  {e}")

        try:
            wishlist = wishlistMainModel.objects.create(owner=owner)
        except Exception as e:
            raise serializers.ValidationError(f"user cart model is not created  {e}")

        return validated_data


# get user details with profile
class accountsUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountsUserProfileModel
        fields = '__all__'

class accountsGetAllUserDetailsSerializer(serializers.ModelSerializer):
    user_profile = accountsUserProfileSerializer(read_only=True, source='accountsUserProfileModel_owner')
    class Meta:
        model = accountsUserModel
        fields = '__all__'
        # exclude = ['id']


class accountsSentOtpWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, required=True)


    def validate(self, data):

        try:
            owner = accountsUserModel.objects.get(email=data.get('email'))
        except:
            raise serializers.ValidationError('Invalid email')


        return data

    class Meta:
        fields = '__all__'


    def create(self, validated_data):
        owner = validated_data.get('owner')
        otp = str(random.randint(1000, 9999))
        owner = accountsUserModel.objects.get(email=validated_data.get('email'))

        try:
            email_otp = accountsUserLoginOtpModel.objects.create(owner = owner, otp=otp, active = True)
        except Exception as e:
            raise serializers.ValidationError(f"otp model did not created{e}")

        subject = 'Hii'
        message = 'your otp '+ ' '+otp +' '+ 'for verification'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[validated_data.get('email')],
        )
        return validated_data


class accountsLoginWithOtpSerializer(serializers.Serializer):
    user_details = serializers.DictField()
    email = serializers.EmailField(max_length=30, required=True)
    otp = serializers.IntegerField(required=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)



    def validate(self, data):

        try:
            user = accountsUserModel.objects.get(email=data.get('email'))
        except:
            raise serializers.ValidationError('user email is not valid')

        try:
            otp = accountsUserLoginOtpModel.objects.get(otp=data.get('otp'), owner = user)
        except:
            raise serializers.ValidationError('otp is invalid')
        if otp.active:
            pass
        else:
            raise serializers.ValidationError('OTP has expired')

        # try:
        #     user_otp = accountsUserLoginOtpModel.objects.get(owner=user)
        # except Exception as e:
        #     raise serializers.ValidationError(f'otp you entered is not belongs to this user {e}')
        #



        refresh = RefreshToken.for_user(user)
        data['refresh'] = refresh
        print(refresh,'-----------refresh')
        data['access'] = refresh.access_token
        print(refresh.access_token,'-------------------access')
        data['user_details'] = accountsGetAllUserDetailsSerializer(user).data


        return data

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        email = validated_data.get('email')
        otp = validated_data.get('otp')

        return validated_data

    # va={'v':'s', 'j':'d', }
    # va['s']="d"

#get user cart
#
# class accountsGetAllUserCartDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = accountsUserCartModel
#         fields = '__all__'
#
# #get user cart by passing-id:
#
# class accountsGetUserCartProductsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = accountsUserCartProductModel
#         fields = '__all__'
#
#         # fields = ('id', 'product', 'product_status', 'status')
#
# class accountsGetUserCartByIdSerializer(serializers.ModelSerializer):
#     products = accountsGetUserCartProductsSerializer(many=True)
#     # print(products,'------------------productdetiasls')
#
#     class Meta:
#         model = accountsUserCartModel
#         # fields = ('id', 'owner', 'products', 'price')
#         fields = '__all__'


