# from django.conf.urls import url
from l4app import views
from django.urls import path

app_name = 'l4app' # l4app wird dann in den Templates genutzt

urlpatterns = [
    path('', views.index,name='index'),
    path('relative', views.relative,name='relative'),
    path('user', views.users_view,name='user'),
    
]