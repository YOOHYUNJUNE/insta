# Generated by Django 4.2.4 on 2023-08-31 08:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_followme"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="followme",
        ),
        migrations.AddField(
            model_name="user",
            name="followings",
            field=models.ManyToManyField(
                related_name="followers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]