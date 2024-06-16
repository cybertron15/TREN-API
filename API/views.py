from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

# from .models import Blogpost
from rest_framework.views import APIView
from .serializers import (
    TaskSerializers,
    GoalSerializers,
    CategorySerializers,
    UserSerializer
)
from .models import Tasks, Goals, Categories
from django.contrib.auth import get_user_model

# getting custom user model
User = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    serializer_class = CategorySerializers
    queryset = Categories.objects.all()

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializers
    # queryset = Tasks.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication]
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
    
    def get_queryset(self):
        user = self.request.user
        return Tasks.objects.filter(owner=user)


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializers
    queryset = Tasks.objects.all()
    authentication_classes = [JWTAuthentication,SessionAuthentication]


class GolasListCreate(generics.ListCreateAPIView):
    serializer_class = GoalSerializers
    queryset = Goals.objects.all()
    authentication_classes = [JWTAuthentication,SessionAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
    
    def get_queryset(self):
        user = self.request.user
        return Goals.objects.filter(owner=user)

class GoalsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializers
    queryset = Goals.objects.all()
    authentication_classes = [JWTAuthentication,SessionAuthentication]

