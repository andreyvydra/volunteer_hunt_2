# Generated by Django 4.0.5 on 2022-06-12 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_employer_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='employer',
            name='link',
            field=models.URLField(max_length=128, null=True, verbose_name='Ссылка на проект или на фонд'),
        ),
    ]
