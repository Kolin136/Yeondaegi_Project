# Generated by Django 4.0 on 2023-05-05 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yeondaegi_app', '0005_organize_like_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organize',
            name='hide_data',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='organize',
            name='like',
            field=models.ManyToManyField(blank=True, null=True, related_name='like_user', to='yeondaegi_app.Sign_up'),
        ),
    ]
