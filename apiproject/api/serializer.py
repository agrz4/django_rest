from rest_framework import serializers
from teachers.models import Teacher
from classes.models import Class
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class_assigned = serializers.StringRelatedField(read_only=True)
    class_assigned_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), source='class_assigned', write_only=True
    )

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'class_assigned', 'class_assigned_id', 'deleted']

class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True
    )

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'students', 'teacher_id', 'deleted']

class TeacherSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subject', 'classes', 'deleted']