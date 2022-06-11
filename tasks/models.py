from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models

from user.models import Volunteer, Employer


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование"
    )

    color = ColorField(
        'Цвет',
        format='hex'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class TaskSettings(models.Model):
    min_volunteer_level = models.IntegerField(
        verbose_name="Минимальный уровень волонтёра"
    )

    min_volunteer_rating = models.IntegerField(
        verbose_name="Минимальный рейтинг волонтёра"
    )

    class Meta:
        verbose_name = "Настройка для задачи"
        verbose_name_plural = "Настройки для задачи"

    def __str__(self):
        return str(self.id)


class Photo(models.Model):
    description = models.TextField(verbose_name="Описание")

    photo = models.ImageField(upload_to="photos/", verbose_name="Фото")

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return self.description[:20]


class Task(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=50,
        help_text="Не более 50 символов"
    )

    volunteers = models.ManyToManyField(
        to=Volunteer,
        related_name="task",
        verbose_name="Волонтёры",
        blank=True

    )

    settings = models.ForeignKey(
        to=TaskSettings,
        on_delete=models.CASCADE,
        verbose_name="Настройка для задачи",
    )

    category = models.ForeignKey(
        to=Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )

    creator = models.ForeignKey(
        to=Employer,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Работодатель",
        related_name='my_tasks'
    )

    description = models.TextField(verbose_name="Описание")

    photos = models.ManyToManyField(to=Photo, verbose_name="Фотографии", blank=True)

    datetime = models.DateTimeField(verbose_name="Время и дата")

    max_volunteer = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество волонтёров",
        blank=True,
    )

    point_on_map = models.CharField(
        max_length=60,
        verbose_name="Метка на карте"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name
