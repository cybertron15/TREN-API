from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions

# from .models import Blogpost
from rest_framework.views import APIView
from .serializers import (
    TaskSerializers,
    GoalSerializers,
    CategorySerializers,
    UserSerializer
)
from .models import Tasks, Goals, Categories
from django.contrib.auth.models import User

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializers
    queryset = Categories.objects.all()

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializers
    queryset = Tasks.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        user = self.request.user
        print(user.__repr__)
        serializer.save(owner=user)


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializers
    queryset = Tasks.objects.all()


class GolasListCreate(generics.ListCreateAPIView):
    serializer_class = GoalSerializers
    queryset = Goals.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class GoalsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializers
    queryset = Goals.objects.all()
