from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('list/',views.repo_list,name='list'),
    path('<name>/details/',views.details,name='details'),
    path('<branch>/files/',views.details,name='details'),
]