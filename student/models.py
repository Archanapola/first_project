import random

from django.db import models
from django.db.models.signals import post_save


BRANCH = (
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('IT', 'IT'),
    ('MECH', 'MECH'),
)

def post_save_student(sender, instance, created, **kwargs):

    if created:

        marks = random.randint(1, 100)
        student_marks = studentMarksModel.objects.create(student=instance, marks=marks, sem=1)
        student_marks.save()
        print(student_marks)

        print(instance, '...created...')
        student_marks.save()
    if not created:
        print(instance, '..not created...')

class studentMainModel(models.Model):
    name = models.CharField(max_length=30)
    dob = models.DateField()
    image = models.ImageField()
    branch = models.CharField(max_length=20, choices=BRANCH)

    def __str__(self):
        # return self.id
        return str(self.name) + " --- " + str(self.id)
post_save.connect(post_save_student, sender=studentMainModel)


SEM = [
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Fourth'),
        ('5', 'Fifth'),
        ('6', 'Sixth'),
        ('7', 'Seventh'),
        ('8', 'Eighth'),
    ]

class studentMarksModel(models.Model):
    student = models.ForeignKey(studentMainModel, on_delete=models.CASCADE, related_name='studentMarksModel_student')
    marks = models.IntegerField()
    sem = models.CharField(max_length=20, choices=SEM)

    def __str__(self):
        # return self.student.name
        return str(self.student.name) + " --- " + str(self.student.id)




class studentMarksMainModel(models.Model):
    student = models.ForeignKey(studentMainModel, on_delete=models.CASCADE, related_name='studentMarksMainModel_student')
    marks = models.ManyToManyField(studentMarksModel, related_name='studentMarksMainModel_marks')



#===========================================================================

#FOR CREATING ALL SEMS AT A TIME
# import random
#
# def post_save_student(sender, instance, created, **kwargs):
#     if created:
#         for sem in range(1, 9):
#             marks = random.randint(1, 100)
#             student_marks = studentMarksModel.objects.create(student=instance, marks=marks, sem=str(sem))
#             student_marks.save()
#
# post_save.connect(post_save_student, sender=studentMainModel)

# def student_final_marks(sender, created, instance, **kwargs):
#     if created:
#         student_main = studentMainModel.objects.get(id=instance.student.id)
#         try:
#             student_marks = studentMarksMainModel.objects.get(student=student_main)
#             print(student_marks,'........student_marks.......')
#         except:
#             student_marks = studentMarksMainModel.objects.create(student=student_main)
#
#         student_marks.marks.add(instance)
#         student_marks.save()
#
#         student = instance.student
#         total_marks = studentMarksModel.objects.filter(student=student)
#         final_marks = sum(marks.marks for marks in total_marks)
#
#         student_marks_main = studentMarksMainModel.objects.filter(student=student_main)
#         student_marks_main.update(FinalMarks=final_marks)
#
# post_save.connect(student_final_marks,sender=studentMarksModel)