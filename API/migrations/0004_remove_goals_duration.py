# Generated by Django 5.0.6 on 2024-05-23 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goals',
            name='duration',
        ),
    ]