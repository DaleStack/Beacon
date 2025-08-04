from social_core.exceptions import AuthForbidden

def save_avatar(backend, user, response, *args, **kwargs):
    """
    Extract avatar_url from GitHub response and save to UserProfile.
    """
    if backend.name == 'github':
        avatar_url = response.get('avatar_url')
        github_username = response.get('login')

        # Create or update UserProfile
        from user.models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.github_username = github_username
        if avatar_url:
            profile.avatar_url = avatar_url
        profile.save()



def require_manual_account_linking(strategy, backend, uid, user=None, *args, **kwargs):
    if user:
        return 
    # Stop here if user doesn't exist — don't create a new one
    raise AuthForbidden(backend)
