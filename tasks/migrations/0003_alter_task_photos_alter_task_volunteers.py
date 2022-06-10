# Generated by Django 4.0.5 on 2022-06-10 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='photos',
            field=models.ManyToManyField(blank=True, to='tasks.photo', verbose_name='Фотографии'),
        ),
        migrations.AlterField(
            model_name='task',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='task', to='user.volunteer', verbose_name='Волонтёры'),
        ),
    ]
