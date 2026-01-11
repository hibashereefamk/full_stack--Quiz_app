from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (UserViewset,CategoryViewset,
                    OptionViewset,SubmitQuizView,
                    QuestionViewSet,
                    QuizAttemptViewset,QuizViewset,
                    RegisterView)

rounter =DefaultRouter()

rounter.register(r'users',UserViewset,basename='user')
rounter.register(r'categories',CategoryViewset,basename='category')
rounter.register(r'options',OptionViewset,basename='options')
rounter.register(r'questions',QuestionViewSet,basename='questions')
rounter.register(r'quizzess',QuizViewset,basename='quiz')
rounter.register(r'attemplts',QuizAttemptViewset,basename='quiz_attempt')


urlpatterns = [
    path('',include(rounter.urls)),
    path('api/register/',RegisterView.as_view(),name='auth_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('submit/', SubmitQuizView.as_view(), name='submit-quiz'),
]
