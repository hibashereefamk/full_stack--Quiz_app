from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated,BasePermission,AllowAny
from rest_framework.decorators import action
from .permission import  IsAdmin
from django.contrib.auth import get_user_model
from .models import Question, Quiz, QuizAttempt, Option, Category
# FIX: Imported the correctly spelled serializers
from .serializers import (
    QuizCreatedSerializer, UserSerializer,RegisterSerializer,
    QuizSerializer, QuestionSerializer,
    OptionSerializer, QuizAttemptSerializer,
    QuestionCreateUpdateSerializer, CategorySerializer,
    OptionCreateUpdateSerializer, CategoryCreateUpdateSerializer,QuizListSerializer,
)

User =get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Check if role is Teacher OR Admin
        return getattr(request.user, 'role', '') in ['teacher', 'admin']


class RegisterView(generics.CreateAPIView):
    Queryset =User.objects.all()
    permission_class=[AllowAny]
    serializer_class=RegisterSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return QuestionCreateUpdateSerializer
        return QuestionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]

class OptionViewset(viewsets.ModelViewSet):
    queryset = Option.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OptionCreateUpdateSerializer
        return OptionSerializer

    def get_permissions(self):
       
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]

class CategoryViewset(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsTeacherOrAdmin()]


class QuizViewset(viewsets.ModelViewSet):
    
    queryset = Quiz.objects.all()

    def get_serializer_class(self):
        if self.action =='list_by_category':
            return QuizListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return QuizCreatedSerializer
        return QuizSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve','list_by_category']:
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]
    
    @action(detail=False,methods=['get'],url_path='category/(?P<category_id>\d+)')
    def list_by_category(self,request, category_id=None):
       quizzes = self.queryset.filter(category__id=category_id) 
       serializer = self.get_serializer(quizzes, many=True)
       return Response(serializer.data)

# You didn't have a view for QuizAttempt, so I added it here
class QuizAttemptViewset(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all()
    serializer_class = QuizAttemptSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # Students see only their own attempts; Teachers see all
        user = self.request.user
        if getattr(user, 'role', '') == 'student':
            return QuizAttempt.objects.filter(user=user)
        return QuizAttempt.objects.all()

class SubmitQuizView(APIView):
    def post(self, request):
        data = request.data
        quiz_id = data.get('quiz_id')
        user_answers = data.get('answers') # Format: {question_id: option_id}

        quiz = get_object_or_404(Quiz, id=quiz_id)
        total_marks = 0
        score = 0
        
        # Prepare detailed results to send back
        results = []

        # Iterate over all questions in the quiz
        for question in quiz.questions.all():
            total_marks += question.marks
            
            # Get the user's selected option ID for this question
            selected_option_id = user_answers.get(str(question.id))
            
            correct_option = question.options.filter(is_correct=True).first()
            is_correct = False
            
            # Check if user answered correctly
            if selected_option_id and int(selected_option_id) == correct_option.id:
                score += question.marks
                is_correct = True
            
            results.append({
                'question': question.text,
                'user_selected': int(selected_option_id) if selected_option_id else None,
                'correct_option': correct_option.id,
                'correct_text': correct_option.text,
                'is_correct': is_correct,
                'explanation': "Explanation text here if you have it in your model"
            })

        # Save the attempt to the database
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score
        )

        return Response({
            'score': score,
            'total_marks': total_marks,
            'percentage': (score / total_marks) * 100,
            'results': results # Send this back so frontend can show green/red boxes
        }, status=status.HTTP_200_OK)

