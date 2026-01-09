from rest_framework import serializers
from .models import Question, Quiz, QuizAttempt, Option, Category, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'phone_number', 'role']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# FIX: Added (serializers.ModelSerializer)
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
        fields = ['id', 'title', 'category', 'created_by', 'total_marks', 'time_limit', 'questions']

# FIX: Fixed spelling of Serializer
class QuizCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        # FIX: Checked field name consistency (total_marks)
        fields = ['title', 'category', 'total_marks', 'time_limit']

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