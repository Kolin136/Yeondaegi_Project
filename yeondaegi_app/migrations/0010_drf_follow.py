# Generated by Django 4.0 on 2023-05-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yeondaegi_app', '0009_rename_user_profile_user_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='DRF_Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('friend', models.CharField(max_length=20)),
            ],
        ),
    ]
