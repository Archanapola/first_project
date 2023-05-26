from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
# create user
class productCreateProductCreateAPiView(CreateAPIView):
    serializer_class = productCreateProductSerializer

    def post(self, request):
        serializer = productCreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'PRODUCTS CREATED SUCCESSFULLY'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# productGetProductsWithImagesSerializer
class productGetAllUserProductsListAPIView(ListAPIView):
    queryset = productMainModel.objects.all()
    serializer_class = productGetProductsWithImagesSerializer
    pagination_class = LimitOffsetPagination

    # def get(self, request, *args, **kwargs):
    #     query = productMainModel.objects.all()
    #     serializer = productGetProductsWithImagesSerializer(query, many=True)
    #     return Response(serializer.data)

class productCreateProductWithMultipleImagesCreateAPiView(CreateAPIView):
    serializer_class = productCreateProductWithMultipleImagesSerializer

    def post(self, request):
        serializer = productCreateProductWithMultipleImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'PRODUCTS CREATED SUCCESSFULLY'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class productAddProductToCartCreateAPiView(CreateAPIView):
    serializer_class = productAddProductToCartSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = productAddProductToCartSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'PRODUCTS ADDED TO CART SUCCESSFULLY'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class productGetAllUserCartDetailsListAPIView(ListAPIView):
    queryset = accountsUserCartModel.objects.all()
    serializer_class = productGetAllUserCartDetailsSerializer
    pagination_class = LimitOffsetPagination
    #
    # def get(self, request, formate=None):
    #     # query =self.get_queryset(self)
    #     query = accountsUserModel.objects.all()
    #     serializer = accountsGetUserCartSerializer(query, many=True)
    #     return Response(serializer.data)
    #

class productUserCartByIdDetailsListAPIView(ListAPIView):
    queryset = accountsUserCartModel.objects.all()
    serializer_class = productGetUserCartByIdSerializer
    pagination_class = LimitOffsetPagination

    # def get_queryset(self):
    #     id = self.kwargs['id']  # get the id parameter from kwargs
    #     return accountsUserCartModel.objects.filter(id=id)

    def list(self, request, *args, **kwargs):
        id = kwargs['id']
        queryset = self.filter_queryset(self.get_queryset().filter(id=id))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
# class productAddProductToWishlistCreateAPiView(CreateAPIView):
#     serializer_class = productAddProductToWishlistSerializer
#     authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = productAddProductToWishlistSerializer(data=request.data, context={'request':request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'PRODUCTS ADDED TO CART SUCCESSFULLY'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)