# Generated by Django 5.0.3 on 2024-03-20 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0006_recommendationchoice_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchoice',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.customuser'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.customuser'),
        ),
    ]