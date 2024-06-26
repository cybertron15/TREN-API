# Generated by Django 5.0.6 on 2024-05-29 20:55

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('performance', models.IntegerField(choices=[(1, 'unacceptable'), (2, 'poor'), (3, 'average'), (4, 'good'), (5, 'excellent')], default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('summary', models.TextField(blank=True, max_length=200)),
                ('improvements', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('deadline', models.DateTimeField()),
                ('worked_for', models.DurationField()),
                ('completion', models.FloatField()),
                ('priority', models.IntegerField(choices=[(1, 'High'), (2, 'Midium'), (3, 'Low')], default=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='API.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('task_type', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField()),
                ('did_start_on_time', models.BooleanField()),
                ('actual_start_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('completion', models.FloatField()),
                ('priority', models.IntegerField(choices=[(1, 'High'), (2, 'Midium'), (3, 'Low')], default=3)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='API.categories')),
                ('parent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='API.tasks')),
                ('related_goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='API.goals')),
            ],
        ),
        migrations.CreateModel(
            name='TaskPerformace',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('performance', models.IntegerField(choices=[(1, 'unacceptable'), (2, 'poor'), (3, 'average'), (4, 'good'), (5, 'excellent')], default=1)),
                ('reasons', models.TextField(blank=True, max_length=100)),
                ('summary', models.TextField(blank=True, max_length=100)),
                ('tomorrows_plan', models.TextField(blank=True, max_length=100)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taks_review', to='API.journal')),
                ('related_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfromance', to='API.tasks')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('bio', models.CharField(blank=True, max_length=20)),
                ('profilepic', models.URLField(blank=True)),
                ('settings', models.JSONField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='tasks',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='journal',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='goals',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='categories',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL),
        ),
    ]
