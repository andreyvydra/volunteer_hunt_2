from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Prefetch
from django.apps import apps


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class VolunteerManager(models.Manager):
    def get_volunteer_with_tasks(self):
        return self.prefetch_related(
            Prefetch(
                'task',
                queryset=apps.get_model('user.Volunteer').objects.filter(volunteers=self)
            )
        )
