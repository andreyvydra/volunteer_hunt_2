# Generated by Django 4.0.5 on 2022-06-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_user_username_alter_employer_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='static/users/avatars/', verbose_name='Аватар'),
        ),
    ]
