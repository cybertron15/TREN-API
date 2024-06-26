# Generated by Django 5.0.6 on 2024-05-30 19:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_categories_owner_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL),
        ),
    ]
