from django.db import models
import uuid

# Create your models here.
class Priority(models.IntegerChoices):
    HIGH = 1,'High'
    MID = 2,'Midium'
    LOW = 3,'Low'

class Performace(models.IntegerChoices):
        UNACCEPTABLE = 1,'unacceptable'
        POOR = 2,'poor'
        AVERAGE = 3,'average'
        GOOD = 4,'good'
        EXCELLENT = 5,'excellent'

class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User' ,related_name='category', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Goals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User' ,related_name='goals', on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    category = models.ForeignKey('API.Categories' ,related_name='goals', on_delete=models.CASCADE)
    worked_for = models.DurationField()
    completion =models.FloatField()
    priority = models.IntegerField(choices=Priority.choices, default=3)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User' ,related_name='tasks', on_delete=models.CASCADE)
    related_goal = models.ForeignKey('API.Goals' ,related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category = models.ForeignKey('API.Categories' ,related_name='tasks', on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20) # long or short like drink glass of water
    start_time = models.DateTimeField()
    did_start_on_time = models.BooleanField()
    actual_start_time = models.DateTimeField()
    duration = models.DurationField()
    completion = models.FloatField()
    priority = models.IntegerField(choices=Priority, default=3)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, related_name='subtasks') # foreign key for the same model as some taks may have subtasks

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
    owner = models.ForeignKey('auth.User' ,related_name='journal', on_delete=models.CASCADE)
    performance = models.IntegerField(choices=Performace, default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(max_length=200, blank=True)
    improvements = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name



