from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from user.managers import UserManager, VolunteerManager


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    username = models.CharField(unique=True, max_length=64, null=True)
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=64, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64, blank=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='users/avatars/')
    telegram_id = models.CharField(verbose_name="ID Телеграма", unique=True, max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Volunteer(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    level = models.IntegerField(verbose_name="Уровень")
    objects = VolunteerManager()

    class Meta:
        verbose_name = "Волонтёр"
        verbose_name_plural = "Волонтёры"

    def __str__(self):
        return str(self.user)


class Employer(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатели"

    def __str__(self):
        return str(self.user)
