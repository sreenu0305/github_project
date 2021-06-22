from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('list/',views.repo_list,name='list'),
    path('<name>/details/',views.details,name='details'),
    path('<name>/files/',views.details,name='details'),
    path('<name>/create_branch/',views.create_branch,name='create_branch'),
    path('<name>/save_branch/',views.save_branch,name='save_branch'),
]