from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (UserViewset,CategoryViewset,
                    OptionViewset,
                    QuestionViewSet,
                    QuizAttemptViewset,QuizViewset,)

rounter =DefaultRouter()

rounter.register(r'users',UserViewset,basename='user')
rounter.register(r'categories',CategoryViewset,basename='category')
rounter.register(r'options',OptionViewset,basename='options')
rounter.register(r'questions',QuestionViewSet,basename='questions')
rounter.register(r'quizzess',QuizViewset,basename='quiz')
rounter.register(r'attemplts',QuizAttemptViewset,basename='quiz_attempt')

urlpatterns = [
    path('',include(rounter.urls)),
]
