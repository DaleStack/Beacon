from django.db import models
from django.contrib.auth.models import User

class FavoriteRepo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    repo_name = models.CharField(max_length=200)
    repo_owner = models.CharField(max_length=100)
    repo_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'repo_url')  # Prevent duplicates

    def __str__(self):
        return f"{self.repo_owner}/{self.repo_name}"
