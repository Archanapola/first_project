from rest_framework.authentication import SessionAuthentication,BasicAuthentication

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication

from wishlist.api_admin_v1.serializers import *


class wishlistAddProductToWishlistCreateAPiView(CreateAPIView):
    serializer_class = wishlistAddProductToWishlistSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = wishlistAddProductToWishlistSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class wishlistGetAllWishlistDetailsListAPIView(ListAPIView):
    queryset = wishlistMainModel.objects.all()
    serializer_class = wishlistGetAllwishlistDetailsSerializer
    pagination_class = LimitOffsetPagination

class wishlistUserWishlistByIdDetailsListAPIView(ListAPIView):
    queryset = wishlistMainModel.objects.all()
    serializer_class = wishlistGetUserWishlistByIdSerializer
    pagination_class = LimitOffsetPagination



    def list(self, request, *args, **kwargs):
        id = kwargs['id']
        try:
            wish = wishlistMainModel.objects.get(id=id)
        except:
            return Response({'message': 'wishlist not exist for this is '})
        queryset = self.filter_queryset(self.get_queryset().filter(id=wish.id))
        print(queryset,'---wierfcnejnc')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

