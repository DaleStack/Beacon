from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        github_username = instance.username  # GitHub username is used as User.username
        UserProfile.objects.create(user=instance, github_username=github_username)
