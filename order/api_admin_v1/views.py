from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import *
from order.api_admin_v1.serializers import orderCreateOrderSerializer, orderGetAllOrdersDetailsSerializer, \
    orderUpdateStatusSerializer, orderGetOrdersByUserIdSerializer


class orderCreateOrderAPiView(CreateAPIView):
    serializer_class = orderCreateOrderSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = orderCreateOrderSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'order has been created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class orderGetAllOrdersDetailsListAPIView(ListAPIView):
    queryset = orderMainModel.objects.all()
    serializer_class = orderGetAllOrdersDetailsSerializer
    pagination_class = LimitOffsetPagination



class orderUpdateStatusAPIView(RetrieveUpdateAPIView):
    queryset = orderMainModel.objects.all()
    serializer_class = orderUpdateStatusSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def put(self, request,pk,  *args, **kwargs):
        try:
            queryset = orderMainModel.objects.get(id=pk)
            print(queryset)
        except Exception as e:
            return Response('id is invalid ')
        # order = self.get_object()
        # print(order,'----------------order biewewew')
        serializer = orderUpdateStatusSerializer(data=request.data,instance=queryset, context={'order_id':pk,'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class orderGetUserOrdersListAPIView(ListAPIView):
    queryset = orderMainModel.objects.all()
    serializer_class = orderGetOrdersByUserIdSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, id, *args, **kwargs):
        try:
            owner_det = accountsUserModel.objects.get(id=id)
        except:
            return Response({'message':'user does not exist'})

        queryset = self.filter_queryset(self.get_queryset().filter(owner=owner_det))
        print(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)