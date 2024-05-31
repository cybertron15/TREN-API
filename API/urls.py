from django.urls import path, include
from . import views  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path("category/",views.CategoryListCreate.as_view(), name='category-list-create'),
    path("tasks/",views.TaskListCreate.as_view(), name='task-list-create'),
    path("tasks/<str:pk>",views.TaskRetrieveUpdateDestroy.as_view(), name='task-retirve-update-destroy'),
    path("goals/",views.GolasListCreate.as_view(), name='goal-list-create'),
    path("goals/<str:pk>",views.GoalsRetrieveUpdateDestroy.as_view(), name='goal-retirve-update-destroy'),
    path("signup/",views.UserCreate.as_view(), name=''),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
