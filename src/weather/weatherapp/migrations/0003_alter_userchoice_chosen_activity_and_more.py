# Generated by Django 5.0.3 on 2024-03-20 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0002_alter_customuser_email_alter_customuser_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchoice',
            name='chosen_activity',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='userchoice',
            name='chosen_city',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='userchoice',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userchoice', to='weatherapp.customuser'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='weatherapp.customuser'),
        ),
    ]