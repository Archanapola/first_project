from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

from .serializers import *
# create user
class accountsCreateUserCreateAPiView(CreateAPIView):
    serializer_class = accountsUserCreateSerializer

    def post(self, request):
        serializer = accountsUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'USER CREATED SUCCESSFULLY'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get user details with profile
class accountsGetAllUserDetailsListAPIView(ListAPIView):
    queryset = accountsUserModel.objects.all()
    serializer_class = accountsGetAllUserDetailsSerializer
    pagination_class = LimitOffsetPagination

    # def get(self, request, formate=None):
    #     # query =self.get_queryset(self)
    #     query = accountsUserModel.objects.all()
    #     serializer = accountsGetAllUserDetailsSerializer(query, many=True)
    #     return Response(serializer.data)


# send otp with email
class accountsSendOtpCreateApiView(CreateAPIView):
    serializer_class = accountsSentOtpWithEmailSerializer

    def post(self, request):
        serializer = accountsSentOtpWithEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'OTP SENT SUCCESSFULLY'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class accountsLoginWithOtpCreateApiView(CreateAPIView):
    serializer_class = accountsLoginWithOtpSerializer

    def post(self, request):
        serializer = accountsLoginWithOtpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class accountsGetAllUserCartDetailsListAPIView(ListAPIView):
#     queryset = accountsUserCartModel.objects.all()
#     serializer_class = accountsGetAllUserCartDetailsSerializer
#     pagination_class = LimitOffsetPagination
#     #
#     # def get(self, request, formate=None):
#     #     # query =self.get_queryset(self)
#     #     query = accountsUserModel.objects.all()
#     #     serializer = accountsGetUserCartSerializer(query, many=True)
#     #     return Response(serializer.data)
#     #
#
# class accountsUserCartByIdDetailsListAPIView(ListAPIView):
#     queryset = accountsUserCartModel.objects.all()
#     serializer_class = accountsGetUserCartByIdSerializer
#     pagination_class = LimitOffsetPagination
#
#     # def get_queryset(self):
#     #     id = self.kwargs['id']  # get the id parameter from kwargs
#     #     return accountsUserCartModel.objects.filter(id=id)
#
#     def list(self, request, *args, **kwargs):
#         id = kwargs['id']
#         print(id ,'---id')
#         queryset = self.filter_queryset(self.get_queryset().filter(id=id))
#         print(queryset,'---wierfcnejnc')
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

    # def get(self, request,id, formate=None):
    #     print(id,'-----id in views')
    #     query = accountsUserCartModel.objects.get(id=id)
    #     print(query,'-------------query')
    #     serializer = accountsGetUserCartByIdSerializer(query)
    #     # return Response({'message':'OTP SENT SUCCESSFULLY'})
    #     return Response(serializer.data)
