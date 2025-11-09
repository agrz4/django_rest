from django.db import models
from django.contrib.auth import get_user_model
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

User = get_user_model()

class Teacher(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)

    def __str__(self):
        return self.name
