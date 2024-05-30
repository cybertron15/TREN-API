from rest_framework import serializers
from .models import Tasks,Goals, Categories
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # since user has reverse relation to these fields it wont be added to the User Serializer by default so we add it 
    # goals = serializers.PrimaryKeyRelatedField(many=True, queryset=Tasks.objects.all())
    # tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Tasks.objects.all())

    # instead of adding primarykeyrelated field we can use slugrelated field so we can get the human redable data instead of id's
    # but the slug field column should be unique.
    # goals = serializers.SlugRelatedField(many=True, queryset=Tasks.objects.all(), slug_field='name')
    # tasks = serializers.SlugRelatedField(many=True, queryset=Tasks.objects.all(), slug_field='name')
    re_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            'id','first_name','last_name','username','email','password','re_password'
        ]
    
    def validate(self, data):
        # Call super to run default validations
        data = super().validate(data)

        # Validate password using Django's built-in password validators
        password = data.get('password')
        if password:
            validate_password(password)

        # Check if the password and re-entered password match
        if password != data.get('re_password'):
            raise serializers.ValidationError("The passwords do not match.")

        # Pop out the re-entered password before returning the validated data
        data.pop('re_password')

        return data

class CategorySerializers(serializers.ModelSerializer):
    # we are making the owner field readonly so no one can modify it via serializer data directly.
    # we'll examine the request for authentication headers and set the owner
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Categories
        fields = [
            "id", "name","owner", "created_on"
        ]

class GoalSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.SlugRelatedField(slug_field='name', queryset=Categories.objects.all())
    class Meta:
        model = Goals
        fields = [
            "id",
            "name",
            "owner",
            "deadline",
            "category",
            "worked_for",
            "completion",
            "priority"
        ]

class TaskSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    related_goal = serializers.SlugRelatedField(slug_field='name', queryset=Goals.objects.all())

    class Meta:
        model = Tasks
        fields = [
            "id",
            "owner",
            "related_goal",
            "name",
            "category",
            "task_type",
            "start_time",
            "did_start_on_time",
            "duration",
            "completion",
            "parent",
            "priority"
        ]