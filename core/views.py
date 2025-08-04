from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from django.core.paginator import Paginator

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
    page = request.GET.get("page", 1)  # <-- 👈 new

    query = f"label:{label} state:open"
    if language:
        query += f" language:{language}"

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
        total_count = min(issue_data.get("total_count", 0), 1000)  # GitHub caps at 1000 results
        for item in issue_data.get("items", []):
            repo_api_url = item["repository_url"]
            repo_response = requests.get(repo_api_url, headers=headers)

            if repo_response.status_code == 200:
                repo = repo_response.json()
                cards.append({
                    "repo_name": repo["full_name"],
                    "repo_url": repo["html_url"],
                    "description": repo["description"],
                    "language": repo["language"],
                    "stars": repo["stargazers_count"],
                    "issue_title": item["title"],
                    "issue_url": item["html_url"],
                    "labels": [{"name": label["name"]} for label in item.get("labels", [])]
                })

    # Manual pagination context
    current_page = int(page)
    last_page = (total_count // 12) + (1 if total_count % 12 > 0 else 0)

    return render(request, "core/pages/dashboard.html", {
        "cards": cards,
        "current_page": current_page,
        "last_page": last_page,
    })



def custom_logout(request):
    logout(request)
    return redirect('/')
