# from rest_framework import status
from django_filters import filters
from rest_framework import generics, status
import django_filters
from rest_framework import filters

from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

#CREATE-VEHICLE
class vehicleCreateVehicleGenericView(CreateAPIView):
    # queryset = studentMainModel
    serializer_class = vehicleCreateVehicleSerializer
    def post(self, request):
        print(request,'....request')
        print(self,'.........self')

        serializer = vehicleCreateVehicleSerializer(data = request.data)
        print(request.data,'..................request_data')

        if serializer.is_valid():
            serializer.save()
            print(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#GET-ALL-VEHICLE
class vehicleMainModelFilter(django_filters.FilterSet):
    class Meta:
        model = vehicleMainModel
        # fields = "__all__"
        fields = ["title",'vehicle_no','status']

class vehicleGetAllVehiclesListAPIView(ListAPIView):
    queryset = vehicleMainModel.objects.all()
    serializer_class = vehicleGetAllVehicleSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_class = vehicleMainModelFilter
    search_fields = ['title', 'vehicle_no', 'id', 'status']
    # pagination_class = LimitOffsetPagination

    # def get(self, request, *args, **kwargs):
    #     print(self, '------------self')
    #     print(request,'-------------request')
    #     print(args,'------------args')
    #     print(kwargs,'-----kwargs')
    #     query = vehicleMainModel.objects.all()
    #     print(query,'-----------query')
    #     serializer = vehicleGetAllVehicleSerializer(query, many=True)
    #     print(serializer,'-------------aer')
    #     return Response(serializer.data)


#BREAKDOWN-WITH-IMAGE
class vehicleBreakdownWithImageGenericView(RetrieveAPIView):
    queryset = vehicleBreakdownModel.objects.all()
    serializer_class = vehicleBreakdownWithImageSerializer


    def post(self, request):
        serializer = vehicleBreakdownWithImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        query = vehicleBreakdownModel.objects.all()
        serializer = vehicleBreakdownDetails(query, many=True)
        return Response(serializer.data)

class vehicleBreakdownFilter(django_filters.FilterSet):

    class Meta:
        model = vehicleBreakdownModel
        fields = "__all__"

class VehicleBreakdownDetailsAPIView(generics.ListAPIView):
    queryset = vehicleBreakdownModel.objects.all()
    serializer_class = vehicleBreakdownDetails
    pagination_class = LimitOffsetPagination
    search_fields = ['vehicle__id', 'status', 'id', 'owner__id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_class = vehicleBreakdownFilter

    # filter_class = vehicleBreakdownFilter
    # filter_backends = [filters.DjangoFilterBackend, filters.SearchFilter]
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['vehicle_id', 'status','breakdown_id', 'owner_id']
    # filter_fields = ("vehicle_id", "status",)


    # def get_queryset(self):
    #     queryset = vehicleBreakdownModel.objects.all()
    #     vehicle_id = self.request.query_params.get('vehicle_id', None)
    #     breakdown_id = self.request.query_params.get('breakdown_id', None)
    #     owner_id = self.request.query_params.get('owner_id', None)
    #     status = self.request.query_params.get('status', None)
    #
    #     if vehicle_id is not None:
    #         queryset = queryset.filter(vehicle_id=vehicle_id)
    #     if breakdown_id is not None:
    #         queryset = queryset.filter(id=breakdown_id)
    #     if owner_id is not None:
    #         queryset = queryset.filter(owner=owner_id)
    #     if status is not None:
    #         queryset = queryset.filter(status=status)




# class VehicleBreakdownDetailsAPIView(ListAPIView):
#     queryset = vehicleBreakdownModel.objects.all()
#     serializer_class = vehicleBreakdownDetails
#
#     def get(self, request, *args, **kwargs):
#         query = vehicleBreakdownModel.objects.all()
#         serializer_class = vehicleBreakdownDetails(query, many=True)
#         list_serializer_class = vehicleBreakdownDetails
#         # return Response(serializer.data)

#USER ASSIGNED TO BREAKDOWN:
class vehicleAssignBreakdownToUserCreateAPIView(CreateAPIView):
    queryset = vehicleBreakdownModel.objects.all()
    serializer_class = vehicleAssignToUserSerializer

    def post(self, request):
        serializer = vehicleAssignToUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user is assigned succesfully'})
            # return Response({'message':'done'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# INSPECTION WITH IMAGE:
class vehicleInspectionWithImageGenericView(RetrieveAPIView):
    queryset = vehicleBreakdownModel.objects.all()
    serializer_class = vehicleInspectionWithImageSerializer

    def post(self, request):
        serializer = vehicleInspectionWithImageSerializer(data=request.data)
        if serializer.is_valid():
             serializer.save()
             return Response({'message':'Success '})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# REPAIR WITH IMAGE:
# class vehicleRepairWithImageGenericView(RetrieveAPIView):
#     queryset = vehicleBreakdownModel.objects.all()
#     serializer_class = vehicleRepairWithImageSerializer
#
#     def post(self, request):
#         serializer = vehicleRepairWithImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'VEHICLE is in repaired'})
#
#             # return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# BREAKDOWN HISTORY WITH ID
class vehicleGetAllBreakdownDetailsByIdListView(ListAPIView):
    queryset = vehicleBreakdownModel.objects.all()
    serializer_class = vehicleGetAllBreakdownDetailsByIdSerializer

    def get(self, request, id, *args, **kwargs):
        query = vehicleBreakdownModel.objects.filter(vehicle__id=id)
        serializer = vehicleGetAllBreakdownDetailsByIdSerializer(query, many=True)
        return Response(serializer.data)















    # def get(self, request, id):
    #     instance = self.queryset.filter(id=id).first()
    #     if instance is not None:
    #         serializer = self.serializer_class(instance)
    #         return Response(serializer.data)
    #     return Response({'error': 'Instance not found.'}, status=status.HTTP_404_NOT_FOUND)


# class vehicleBreakdownWithImageGenericView(RetrieveAPIView):
#     queryset = vehicleBreakdownModel.objects.all()
#     serializer_class = vehicleBreakdownWithImageSerializer
#
#     def post(self, request):
#         serializer = vehicleBreakdownWithImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#