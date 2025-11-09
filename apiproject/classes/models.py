from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Class(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=50)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True, related_name='classes')

    def __str__(self):
        return self.name
