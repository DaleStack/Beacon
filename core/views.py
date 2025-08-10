from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
import os
from dotenv import load_dotenv
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from favorites.models import FavoriteRepo
from favorites.forms import FavoriteRepoForm
import hashlib
from django.core.cache import cache


load_dotenv()


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    headers = {
        "Accept": "application/vnd.github+json"
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    label = request.GET.get("label", "good-first-issue")
    language = request.GET.get("language")
    topic = request.GET.get("topic", "")
    page = request.GET.get("page", 1)

    query = f"label:{label} state:open"
    if language:
        query += f" language:{language}"
    if topic:
        query += f" {topic} in:title,body"

    # Generate a unique cache key for the issue search
    query_string = f"{label}_{language}_{topic}_page{page}"
    cache_key = f"github_issues_{hashlib.md5(query_string.encode()).hexdigest()}"
    cached_data = cache.get(cache_key)

    if cached_data:
        cards, total_count = cached_data
    else:
        issues_url = "https://api.github.com/search/issues"
        params = {
            "q": query,
            "sort": "created",
            "order": "desc",
            "per_page": 9,
            "page": page
        }

        issue_response = requests.get(issues_url, headers=headers, params=params)

        cards = []
        total_count = 0
        if issue_response.status_code == 200:
            issue_data = issue_response.json()
            total_count = min(issue_data.get("total_count", 0), 1000)

            for item in issue_data.get("items", []):
                repo_api_url = item["repository_url"]
                repo_cache_key = f"repo_{hashlib.md5(repo_api_url.encode()).hexdigest()}"
                repo = cache.get(repo_cache_key)

                if not repo:
                    repo_response = requests.get(repo_api_url, headers=headers)
                    if repo_response.status_code == 200:
                        repo = repo_response.json()
                        cache.set(repo_cache_key, repo, timeout=60 * 60)  # Cache repo for 1 hour

                if repo:
                    cards.append({
                        "repo_name": repo["name"],
                        "repo_owner": repo["owner"]["login"],
                        "repo_url": repo["html_url"],
                        "description": repo["description"],
                        "language": repo["language"],
                        "stars": repo["stargazers_count"],
                        "issue_title": item["title"],
                        "issue_url": item["html_url"],
                        "labels": [{"name": label["name"]} for label in item.get("labels", [])]
                    })

        # Cache the final cards and count for 5 minutes
        cache.set(cache_key, (cards, total_count), timeout=60 * 5)

    # Manual pagination context
    current_page = int(page)
    last_page = (total_count // 12) + (1 if total_count % 12 > 0 else 0)

    return render(request, "core/pages/dashboard.html", {
        "cards": cards,
        "current_page": current_page,
        "last_page": last_page,
        "topic": topic,
    })


def custom_logout(request):
    logout(request)
    return redirect('/')
