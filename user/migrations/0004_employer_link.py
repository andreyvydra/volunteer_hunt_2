# Generated by Django 4.0.5 on 2022-06-12 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_telegram_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='link',
            field=models.CharField(max_length=128, null=True, verbose_name='Ссылка на проект или на фонд'),
        ),
    ]
