""" views for github project"""
from django.shortcuts import render, reverse
from github import Github
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    """For home page"""
    return render(request, 'git/index.html')


open_git = ""
user_name = ''
branch = ''
pulls = ''
list_all = ''


def repo_list(request):
    """To display all repositories in git"""
    if request.method == "POST":
        global open_git
        open_git = Github(request.POST["token"])
        global user_name
        user_name = request.POST['username']
        user = open_git.get_user(user_name).get_repos()
        print(dir(open_git))
        list_all = []
        for each in user:
            list_all.append(each)
        return render(request, 'git/rep_list.html', {"list": list_all, "name": user_name})
    else:
        return render(request, 'git/index.html')


def details(request, name):
    """ details of repository and branches of repository"""
    print(user_name)
    print('hello')
    print(type(open_git))
    repo = open_git.get_repo("{}/{}".format(user_name, name))
    global branch
    branch = list(repo.get_branches())
    print(branch)
    global pulls
    if request.method == "POST":
        # import pdb
        # pdb.set_trace()
        contents = repo.get_contents("", ref=request.POST["branch"])
        pulls = repo.get_pulls(state='open', sort='created', base=request.POST["branch"])
    else:
        contents = repo.get_contents("", ref="main")
        pulls = repo.get_pulls(state='open', sort='created', base="master")
    global list_all
    list_all = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            list_all.extend(repo.get_contents(file_content.path))
        else:
            list_all.append(file_content)
    print(contents)
    return render(request, "git/branch.html",
                  {"branch": branch, "files": list_all, "repo": repo, "pulls": pulls})


def create_branch(request, name):
    """ create new branch """
    repo_name = name
    # source_branch = 'master'
    # target_branch = 'sreenu'
    #
    # repo = open_git.get_user().get_repo(repoName)
    # sb = repo.get_branch(source_branch)
    # repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
    return render(request, 'git/create_branch.html', {'name': repo_name, 'branch': branch})


def save_branch(request, name):
    """ save branch"""
    repo = open_git.get_repo("{}/{}".format(user_name, name))
    source_branch = request.POST.get('branch')
    target_branch = request.POST.get("new_branch")
    sourse_branch = repo.get_branch(source_branch)
    repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sourse_branch.commit.sha)
    return HttpResponseRedirect(f'/git/{name}/details/')
    # return HttpResponseRedirect(reverse('details',args=(name,)))


def create_file(request, name):
    """ to create file """
    # open_git.create_file("test.txt", "test", "test", branch="test")
    return render(request, 'git/upload.html', {'name': name, 'branch': branch})


def save_file(request, name):
    """saving file"""
    if request.method == "POST":
        repo = open_git.get_user().get_repo(name)
        repo.create_file(request.FILES["file"].name, request.POST["msg"], request.FILES["file"].read(),
                         branch=request.POST["branch"])
        return render(request, 'git/upload.html', {'name': name})

    else:
        return render(request, "git/upload.html", {"name": name, "branch": branch})


def pull_request(request, name):
    """ creating pull request """
    return render(request, 'git/pull.html', {'name': name, 'branch': branch})


def save_pull_details(request, name):
    """ saving pull request"""
    # import pdb
    # pdb.set_trace()
    repo = open_git.get_user().get_repo(name)
    if request.method == "POST":
        title = request.POST['title']
        body = request.POST['body']
        head = request.POST['head']
        base = request.POST['base']
        new_pull_request = repo.create_pull(title=title, body=body, head=head, base=base)
        print("sreenu")
        print(new_pull_request)
        return HttpResponseRedirect(f'/git/{name}/details/')
    else:
        return render(request, 'git/pull.html', {'name': name, 'branch': branch, 'pulls': pulls})


def merge(request, name):
    """To merge the  branches """
    return render(request, "git/merge.html", {"branches": branch, "name": name})


def save_merge(request, name):
    """ implementing the merge"""
    my_repo = open_git.get_repo("{}/{}".format(user_name, name))
    if request.method == "POST":
        try:
            base = my_repo.get_branch(request.POST["base"])
            head = my_repo.get_branch(request.POST["head"])
            merge_request = my_repo.merge(base, head.commit.sha, "merge to {}".format(base))
            print(merge_request)
        except Exception as ex:
            print(ex)
        return render(request, "git/branch.html", {"branches": branch, "files": list_all, "repo": my_repo})
    else:
        return render(request, "git/merge.html", {"branches": branch, "name": name})
