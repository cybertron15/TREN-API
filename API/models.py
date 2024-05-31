from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import timedelta
# TODO : Please set an automation script to load the category model with 3 default categories when the project is first started
# Create your models here.
class Priority(models.IntegerChoices):
    HIGH = 1,'High'
    MID = 2,'Midium'
    LOW = 3,'Low'

class TaskType(models.IntegerChoices):
    ONETIME = 1,'onetime'
    REGULAR = 2,'regular'

class Performace(models.IntegerChoices):
        UNACCEPTABLE = 1,'unacceptable'
        POOR = 2,'poor'
        AVERAGE = 3,'average'
        GOOD = 4,'good'
        EXCELLENT = 5,'excellent'

# custom user model for storing user auth and other data
class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    bio = models.CharField(max_length=20, blank=True)
    profilepic = models.URLField(blank=True)
    settings = models.JSONField(blank=True, default=dict)

    # this is the field which will be used when loggin in
    USERNAME_FIELD = "email"
    # required field when creating superuser, email and password is required by default
    REQUIRED_FIELDS = ['first_name','last_name','username',]

class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('API.CustomUser' ,related_name='category', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Goals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('API.CustomUser' ,related_name='goals', on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    category = models.ForeignKey('API.Categories' ,related_name='goals', on_delete=models.CASCADE)
    worked_for = models.DurationField(default=timedelta())
    completion =models.FloatField(default=0)
    priority = models.IntegerField(choices=Priority.choices, default=3)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('API.CustomUser' ,related_name='tasks', on_delete=models.CASCADE)
    related_goal = models.ForeignKey('API.Goals' ,related_name='tasks', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey('API.Categories' ,related_name='tasks', on_delete=models.CASCADE)
    task_type = models.IntegerField(choices=TaskType.choices, default=2) # long or short like drink glass of water
    start_time = models.DateTimeField()
    did_start_on_time = models.BooleanField(blank=True)
    actual_start_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(default=timedelta())
    completion = models.FloatField(default=0)
    priority = models.IntegerField(choices=Priority, default=3)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, related_name='subtasks',blank=True, null=True) # foreign key for the same model as some taks may have subtasks

    def __str__(self):
        return self.name

class TaskPerformace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_task = models.ForeignKey('API.Tasks' ,related_name='perfromance', on_delete=models.CASCADE)
    performance = models.IntegerField(choices=Performace, default=1)
    reasons = models.TextField(max_length=100, blank=True)
    summary = models.TextField(max_length=100, blank=True)
    tomorrows_plan = models.TextField(max_length=100, blank=True)
    entry = models.ForeignKey("API.Journal", related_name='taks_review', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Journal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('API.CustomUser' ,related_name='journal', on_delete=models.CASCADE)
    performance = models.IntegerField(choices=Performace, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=200, blank=True)
    improvements = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name



