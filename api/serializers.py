from rest_framework import serializers
from .models import Question, Quiz, QuizAttempt, Option, Category
from django.contrib.auth import get_user_model

User= get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password= serializers.CharField(write_only =True,min_length =8)
    class Meta:
        model =User
        fields =['username','password','email','name','phone_number','role']

    def create(self,validated_data):
            user=User.objects.create_user(

            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            name=validated_data.get('name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role', 'student')
            )
            return user
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'phone_number', 'role']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class OptionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'question', 'text', 'is_correct']


class QuizListSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model = Quiz
       
        fields = ['id', 'title', 'level', 'questions_count', 'total_marks', 'time_limit']   

        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'marks', 'options']

class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'marks']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'category', 'created_by', 'total_marks', 'time_limit', 'questions','level']


class QuizCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
       
        fields = ['title', 'category','level', 'total_marks', 'time_limit']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

# FIX: Fixed spelling of Serializer
class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    
    # FIX: This was dangling in your views.py, I moved it here
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'submitted_at']
