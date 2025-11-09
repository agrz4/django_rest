from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_STUDENT, 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_teacher = (self.role == self.ROLE_TEACHER)
        self.is_student = (self.role == self.ROLE_STUDENT)

        if self.is_superuser:
            self.role = self.ROLE_ADMIN

        super().save(*args, **kwargs)

    def get_role(self):
        return self.role
