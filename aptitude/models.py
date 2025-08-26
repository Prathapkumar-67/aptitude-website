from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# --------------------------
# Custom User Model
# --------------------------

class User(AbstractUser):
    ROLE_CHOICES = [
        ('boss', 'Boss'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    email= models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username


# --------------------------
# Core Entities
# --------------------------

class Topic(models.Model):
    CATEGORY_CHOICES = [
        ('Common', 'Common'),
        ('IT-specific', 'IT-specific'),
        ('Govt-specific', 'Govt-specific'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    display_order = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='topics_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='topics_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    display_order = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subtopics_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='subtopics_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VideoLesson(models.Model):
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    duration = models.IntegerField(help_text="Duration in seconds")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='videos_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='videos_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Note(models.Model):
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file_url = models.FileField(upload_to='notes/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notes_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notes_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resource(models.Model):
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    description = models.TextField()
    link = models.URLField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resources_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resources_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    text = models.TextField()
    time_limit = models.IntegerField(help_text="In seconds")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='questions_created')
    created_at = models.DateTimeField(auto_now_add=True)


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField()


# --------------------------
# User Activity Tracking
# --------------------------

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField(help_text="Time taken in seconds")


class UserStreak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    streak_count = models.IntegerField()


class NotificationSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    enabled = models.BooleanField(default=True)
