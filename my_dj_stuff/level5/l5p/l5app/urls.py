# from django.conf.urls import url
from l5app import views
from django.urls import path


app_name = 'l5app' # l4app wird dann in den Templates genutzt

urlpatterns = [
    path('', views.index,name='index'),
    path('register/', views.register,name='register'),
    path('login/', views.user_login,name='user_login'),
    path('logout/', views.user_logout, name='user_logout')
    
]