# Generated by Django 4.1.7 on 2023-03-29 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='studentMainModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('image', models.ImageField(upload_to='')),
                ('branch', models.CharField(choices=[('CSE', 'CSE'), ('ECE', 'ECE'), ('IT', 'IT'), ('MECH', 'MECH')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='studentMarksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField()),
                ('sem', models.CharField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'), ('7', 'Seventh'), ('8', 'Eighth')], max_length=20)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentMarksModel_student', to='student.studentmainmodel')),
            ],
        ),
        migrations.CreateModel(
            name='studentMarksMainModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.ManyToManyField(related_name='studentMarksMainModel_marks', to='student.studentmarksmodel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentMarksMainModel_student', to='student.studentmainmodel')),
            ],
        ),
    ]
