# Generated by Django 5.0.3 on 2024-03-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0011_alter_userchoice_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchoice',
            name='recommendations',
        ),
        migrations.AddField(
            model_name='userchoice',
            name='recommendations',
            field=models.ManyToManyField(to='weatherapp.recommendationchoice'),
        ),
    ]
