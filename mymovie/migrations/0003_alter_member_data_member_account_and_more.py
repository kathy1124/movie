# Generated by Django 4.2.5 on 2024-05-14 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymovie', '0002_rename_member_member_data_member_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member_data',
            name='member_account',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='member_data',
            name='member_password',
            field=models.CharField(max_length=10),
        ),
    ]
