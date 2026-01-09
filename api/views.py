from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Ensure these are imported correctly from your permissions file
from .permission import IsTeacher, IsAdmin, IsStudent 

from .models import Question, Quiz, QuizAttempt, Option, Category, CustomUser
# FIX: Imported the correctly spelled serializers
from .serializers import (
    QuizCreatedSerializer, UserSerializer,
    QuizSerializer, QuestionSerializer,
    OptionSerializer, QuizAttemptSerializer,
    QuestionCreateUpdateSerializer, CategorySerializer,
    OptionCreateUpdateSerializer, CategoryCreateUpdateSerializer
)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionCreateUpdateSerializer
        return QuestionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsTeacher() | IsAdmin()]

class OptionViewset(viewsets.ModelViewSet):
    queryset = Option.objects.all()

    def get_serializer_class(self):
        # FIX: Spelling of partial_update
        if self.action in ['create', 'update', 'partial_update']:
            return OptionCreateUpdateSerializer
        return OptionSerializer

    def get_permissions(self):
        # FIX: Spelling of retrieve
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin() | IsTeacher()]

class CategoryViewset(viewsets.ModelViewSet):
    # FIX: QuerySet was Option, changed to Category
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin() | IsTeacher()]

class QuizViewset(viewsets.ModelViewSet):
    # FIX: QuerySet was Option, changed to Quiz
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuizCreatedSerializer
        return QuizSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin() | IsTeacher()]

class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

# You didn't have a view for QuizAttempt, so I added it here
class QuizAttemptViewset(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Students see only their own attempts; Teachers see all
        user = self.request.user
        if getattr(user, 'role', '') == 'student':
            return QuizAttempt.objects.filter(user=user)
        return QuizAttempt.objects.all()