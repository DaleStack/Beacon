from django.contrib import admin
from .models import FavoriteRepo

@admin.register(FavoriteRepo)
class FavoriteRepoAdmin(admin.ModelAdmin):
    list_display = ('user', 'repo_owner', 'repo_name', 'created_at')
    search_fields = ('repo_name', 'repo_owner', 'repo_url')
    list_filter = ('user', 'created_at')
