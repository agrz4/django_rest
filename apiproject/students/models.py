from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
# Import Class dari aplikasi classes
from classes.models import Class

class Student(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    age = models.IntegerField()
# Gunakan 'classes.Class' untuk referensi model dari aplikasi lain
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name