""" views for github project"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from github import Github
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from github.ContentFile import ContentFile


def home(request):
    """For home page"""
    return render(request, 'git/index.html', {})


open_git = ""
user_name = ''


def repo_list(request):
    """To display all repositories in git"""
    # import pdb

    if request.method == "POST":
        global open_git
        open_git = Github(request.POST["token"])
        global user_name
        user_name = request.POST['username']
        user = open_git.get_user(user_name).get_repos()
        print(dir(open_git))
        list = []
        for each in user:
            list.append(each)
        return render(request, 'git/rep_list.html', {"list": list, "name": user_name})


def details(request, name):
    """ detailsof repository and branches of repository"""
    # user = open_git.get_user('sreenu0305')
    print(user_name)
    print('hello')
    print(type(open_git))
    repo = open_git.get_repo("{}/{}".format(user_name, name))
    branch = list(repo.get_branches())
    print(branch)
    # import pdb
    # pdb.set_trace()

    return render(request, 'git/branch.html', {'branch': branch})


def files(request,branch):
    repo = open_git.get_repo("{}/{}".format(user_name, branch))
    contents = repo.get_contents("")
    for content_file in contents:

        print(content_file)
    ContentFile(path=".gitignore")
    ContentFile(path="README.md")
    ContentFile(path="sample.yaml")
    return render(request, 'git/files.html')
