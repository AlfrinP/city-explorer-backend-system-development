# Generated by Django 5.0.3 on 2024-03-20 21:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0007_alter_userchoice_user_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
