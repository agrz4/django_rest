# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from teachers.models import Teacher
from classes.models import Class
from students.models import Student
from .serializer import TeacherSerializer, ClassSerializer, StudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def create(self, request, *args, **kwargs):
        # Cek apakah data yang masuk berupa list (untuk bulk create)
        many = isinstance(request.data, list)

        # Inisiasi serializer dengan many=True jika data berupa list
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.select_related('teacher').all()
    serializer_class = ClassSerializer

    def create(self, request, *args, **kwargs):
        # Cek apakah data yang masuk berupa list (untuk bulk create)
        many = isinstance(request.data, list)

        # Inisiasi serializer dengan many=True jika data berupa list
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('class_assigned').all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        # Cek apakah data yang masuk berupa list (untuk bulk create)
        many = isinstance(request.data, list)

        # Inisiasi serializer dengan many=True jika data berupa list
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
