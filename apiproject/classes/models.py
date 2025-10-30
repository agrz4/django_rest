from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
# Import Teacher dari aplikasi teachers
from teachers.models import Teacher

class Class(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50)
# Gunakan 'teachers.Teacher' jika import bermasalah, namun import eksplisit lebih baik
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='classes')

    def __str__(self):
        return self.name
