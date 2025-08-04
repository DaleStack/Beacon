from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=39)  # From GitHub
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)     # Comma-separated
    interests = models.CharField(max_length=255, blank=True)  # Comma-separated

    def __str__(self):
        return self.github_username or self.user.username
