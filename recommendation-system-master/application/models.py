from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.utils import timezone

# Create your models here.

# models for societypy recommendation

class Answer(models.Model):
    text = models.CharField(max_length = 255)
    boolean = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.text} - {self.boolean}'


class Question(models.Model):
    text = models.CharField(max_length = 255)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return self.text


class Combination(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.question} => {self.answer}"

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    question_answers = models.ManyToManyField(Combination)
    timestamp = models.DateTimeField(default = timezone.now)

# models for career recommendation
class Visit(models.Model):
    timestamp = models.DateTimeField(default = timezone.now)

class Dept_Answer(models.Model):
    text = models.CharField(max_length = 255)
    boolean = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.text} - {self.boolean}'


class Dept_Question(models.Model):
    text = models.CharField(max_length = 255)
    answers = models.ManyToManyField(Dept_Answer)

    def __str__(self):
        return self.text


class Dept_Combination(models.Model):
    question = models.ForeignKey(Dept_Question, on_delete = models.CASCADE)
    answer = models.ForeignKey(Dept_Answer, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.question} => {self.answer}"


class Dept_UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    question_answers = models.ManyToManyField(Dept_Combination)
    timestamp = models.DateTimeField(default = timezone.now)

 
