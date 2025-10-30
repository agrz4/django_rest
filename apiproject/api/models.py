from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

# Create your models here.
class Teacher(SafeDeleteModel):
    # Opsi default_manager dan deleted_manager akan otomatis tersedia
    # Cascade behavior saat objek ini dihapus (lunak):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Class(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes')

    def __str__(self):
        return self.name

class Student(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name