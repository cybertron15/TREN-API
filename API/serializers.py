from rest_framework import serializers
from .models import Tasks,Goals, Categories
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
User = get_user_model()
# customized field 
class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super().get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(owner=request.user)

class UserSerializer(serializers.ModelSerializer):
    # since user has reverse relation to these fields it wont be added to the User Serializer by default so we add it 
    # goals = serializers.PrimaryKeyRelatedField(many=True, queryset=Tasks.objects.all())
    # tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Tasks.objects.all())

    # instead of adding primarykeyrelated field we can use slugrelated field so we can get the human redable data instead of id's
    # but the slug field column should be unique.
    # goals = serializers.SlugRelatedField(many=True, queryset=Tasks.objects.all(), slug_field='name')
    # tasks = serializers.SlugRelatedField(many=True, queryset=Tasks.objects.all(), slug_field='name')
    re_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
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
    
    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

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
    # using the custom primary key realated fields difned above so the user can only see the goals which belongs to them
    related_goal = UserFilteredPrimaryKeyRelatedField(queryset=Goals.objects.all(), required=False, allow_null=True)
    parent = UserFilteredPrimaryKeyRelatedField(queryset=Tasks.objects.all(), required=False, allow_null=True)

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
            "actual_start_time",
            "duration",
            "completion",
            "priority",
            "parent"
        ]

    # validating related_goals fields making sure used can only create tasks related to their own goals
    def validate_related_goal(self, value):
        request = self.context.get('request')
        if value and value.owner != request.user:
            raise serializers.ValidationError("You can only relate tasks to your own goals.")
        return value
    
    def validate_parent(self, value):
        request = self.context.get('request')
        if value and value.owner != request.user:
            raise serializers.ValidationError("You can only create subtasks for your own tasks.")
        return value