from rest_framework import generics, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import *
# from student.api_admin_v1.serializers import studentCreateStudentSerializer, studentGetAllStudentSerializer

# from first_project.student.api_admin_v1.serializers import studentGetAllStudentSerializer
# from first_project.student.models import studentMainModel
from ..models import *

class studentCreateStudentGenericView(generics.GenericAPIView):
    # queryset = studentMainModel
    serializer_class = studentCreateStudentSerializer
    def post(self, request):
        serializer = studentCreateStudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response({'message' : 'Done....!'})
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class studentGetAllStudentsListAPIView(ListAPIView):
    queryset = studentMainModel.objects.all()
    serializer_class = studentGetAllStudentSer1ializer
    def get(self, request, *args, **kwargs):
        query = studentMainModel.objects.all()
        serializer = studentGetAllStudentSer1ializer(query, many=True)
        return Response(serializer.data)


class studentAddMarksToStudentGenericView(generics.GenericAPIView):
    # queryset = studentMainModel
    serializer_class = studentAddMarksToStudentSerializer
    def post(self, request):
        serializer = studentAddMarksToStudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response({'message' : 'Done....!'})
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class studentGetAllStudentsMarksListAPIView(RetrieveAPIView):
#     queryset = studentMarksModel.objects.all()
#     serializer_class = studentGetAllStudentFinalMarksSerializer
#     def get(self, request, id, *args, **kwargs):
#         print(id,'=======================')
#         query = studentMarksModel.objects.get(student__id=id)
#         print('query ==================',query)
#         serializer = studentGetAllStudentFinalMarksSerializer(query)
#         return Response(serializer.data)

class studentGetAllStudentsMarksByIdListAPIView(RetrieveAPIView):
    queryset = studentMainModel.objects.all()
    serializer_class = studentGetAllStudentMarksByIdSerializer
    def get(self, request, id, *args, **kwargs):
        print(id,'=======================')
        query = studentMainModel.objects.get(id=id)
        print('query ==================',query)
        serializer = studentGetAllStudentMarksByIdSerializer(query)
        return Response(serializer.data)