from django.shortcuts import render
from github import Github


# Create your views here.

def home(request):
    """For home page"""
    return render(request, 'git/index.html', {})


def repo_list(request):
    """To display all repositories in git"""
    if request.method == "POST":
        git = Github()
        name = request.POST['username']
        user = git.get_user(name)
        print(user)
        r = user.get_repos()
        total = []
        for each in r:
            total.append(each.name)
        return render(request, 'git/rep_list.html', {"list": total, "name": name})
