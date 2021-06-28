from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('list/',views.repo_list,name='list'),
    path('<name>/details/',views.details,name='details'),
    path('<name>/files/',views.details,name='details'),
    path('<name>/create_branch/',views.create_branch,name='create_branch'),
    path('<name>/branch_list/',views.branch_list,name='branch_list'),
    path('<name>/save_branch/',views.save_branch,name='save_branch'),
    path('<name>/create_file/',views.create_file,name='create_file'),
    path('<name>/save_file/',views.save_file,name='save_file'),
    path('<name>/pull/',views.pull_request,name='pull'),
    path('<name>/save_pull/',views.save_pull_details,name='save_pull'),
    path('<name>/merge/',views.merge,name='merge'),
    path('<name>/save_merge/',views.save_merge,name='save_merge'),
    path('<name>/delete_branch/',views.branch_delete,name='delete_branch'),
    path('<name>/delete/',views.delete,name='delete'),
]