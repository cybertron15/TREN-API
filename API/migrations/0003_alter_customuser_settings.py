# Generated by Django 5.0.6 on 2024-05-30 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_alter_customuser_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='settings',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
