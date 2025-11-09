from django.db import models
from django.contrib.auth import get_user_model
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

User = get_user_model()

class Student(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class_assigned = models.ForeignKey('classes.Class', on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name