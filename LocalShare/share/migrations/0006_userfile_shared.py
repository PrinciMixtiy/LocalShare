# Generated by Django 5.0.3 on 2024-09-18 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0005_alter_userfile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfile',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]
