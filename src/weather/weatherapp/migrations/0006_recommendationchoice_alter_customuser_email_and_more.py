# Generated by Django 5.0.3 on 2024-03-20 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0005_alter_userchoice_recommendations'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendationChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userchoice',
            name='recommendations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weatherapp.recommendationchoice'),
        ),
    ]
