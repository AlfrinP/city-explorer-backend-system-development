# Generated by Django 5.0.3 on 2024-03-21 05:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0010_alter_userchoice_recommendations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.customuser'),
        ),
    ]
