from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES=(
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    name=models.CharField(max_length=50)
    phone_number =models.CharField(max_length=15,blank=True,null=True)
    role=models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name=models.CharField(max_length=100)


    def __str__(self):
        return self.name
    

class Quiz(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_by =models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role':'teacher'}
    )
    level=models.CharField(max_length=20,default='Medium')
    total_marks =models.IntegerField()
    time_limit=models.IntegerField(help_text="Time in minutes")


    def __str__(self):
        return self.title
    
class Question(models.Model):
    quiz= models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name='questions')
    text=models.TextField()
    marks=models.IntegerField(default=1)

    def __str__(self):
        return self.text

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


