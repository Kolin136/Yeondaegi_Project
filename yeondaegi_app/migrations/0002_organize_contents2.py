# Generated by Django 4.1.7 on 2023-02-17 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yeondaegi_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organize',
            name='contents2',
            field=models.TextField(default=None),
        ),
    ]
