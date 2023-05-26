from rest_framework import serializers

from ..models import *

class studentCreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = studentMainModel
        fields = '__all__'


class studentGetAllStudentSer1ializer(serializers.ModelSerializer):

    class Meta:
        model = studentMainModel
        fields = '__all__'



class studentAddMarksToStudentSerializer(serializers.ModelSerializer):
    def validate(self, data):
        student = data['student']

        sem = data['sem']
        if student.studentMarksModel_student.filter(sem=sem).exists():
            raise serializers.ValidationError(
                f"A studentMarksModel instance for semester {sem} already exists for this student.")

        return data
    class Meta:
        model = studentMarksModel
        fields = '__all__'

#

class studentGetAllStudentMarksDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = studentMarksModel
        fields = '__all__'


class studentGetAllStudentMarksByIdSerializer(serializers.ModelSerializer):
    student_marks = studentGetAllStudentMarksDetailsSerializer(many=True, read_only=True,source="studentMarksModel_student")

    class Meta:
        model = studentMainModel
        # fields = '__all__'
        fields = ['name', 'dob', 'image', 'branch', 'student_marks']



#=====================================================================================#


# class studentGetAllStudentFinalMarksSerializer(serializers.ModelSerializer):
#     student_main = studentCreateStudentSerializer(read_only=True,source="studentMarksMainModel_student")
#     final_marks = serializers.SerializerMethodField(read_only=True)
#
#     def get_final_marks(self, obj):
#         student = obj.student
#         print(student,'-------------student')
#         try:
#             marks = studentMarksModel.objects.filter(student=student)
#             print(marks,'-=================marks')
#         except:
#             raise serializers.ValidationError('Student marks not found')
#         #
#         semesters = {}
#         for mark in marks:
#             print(mark,'------------mark')
#             if mark.sem not in semesters:
#                 semesters[mark.sem] = []
#                 print("sem==========")
#             semesters[mark.sem].append(mark.marks)
#
#         print(semesters,'==========================semester m')
#
#         final_marks = {}
#         for sem, marks in semesters.items():
#             final_marks[f'Semester {sem}'] = marks
#
#         total_marks = sum(sum(marks) for marks in semesters.values())
#         final_marks['Total Marks'] = total_marks
#
#         return "final_marks"
#
#     class Meta:
#         model = studentMarksMainModel
#         fields = '__all__'

# class studentGetAllStudentFinalMarksSerializer(serializers.ModelSerializer):
#     student_main = studentCreateStudentSerializer()
#     final_marks = serializers.SerializerMethodField(read_only=True)
#
#     def get_final_marks(self, obj):
#         student_marks_main = obj.studentMarksMainModel_student.first()
#         if student_marks_main:
#             return student_marks_main.FinalMarks
#         return None
#
#     class Meta:
#         model = studentMarksModel
#         fields = '__all__'



# class studentGetAllStudentFinalMarksSerializer(serializers.ModelSerializer):
#     student_main = studentCreateStudentSerializer
#     final_marks = serializers.SerializerMethodField(read_only=True)
#     def get_final_marks(self, obj):
#         student = obj.marks.all()
#         try:
#             student = studentMarksModel(student, many=True).data
#             print(student)
#         except:
#             raise serializers.ValidationError('student is not created')
#         return student.data
#
#     class Meta:
#         model = studentMarksModel
#         fields = '__all__'
        # fields = ['id', 'sem', 'marks']
