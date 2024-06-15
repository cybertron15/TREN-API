from django.contrib import admin

# Register your models here.
from .models import Tasks, Categories
from django.contrib.auth import get_user_model

# getting custom user model
User = get_user_model()

admin.site.register([User,Tasks,Categories])
