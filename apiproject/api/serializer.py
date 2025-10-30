from rest_framework import serializers
from .models import Teacher, Class, Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'class_assigned', 'deleted']

class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
# Gunakan PrimaryKeyRelatedField untuk field ForeignKey saat membuat/mengupdate
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True
    )

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'students', 'teacher_id']
        read_only_fields = ['teacher']

class TeacherSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subject', 'classes', 'deleted']