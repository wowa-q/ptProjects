# from django.conf.urls import url
from l3_app import views
from django.urls import path


urlpatterns = [
    path('', views.index,name='index'),
    path('form', views.form_name_view,name='form'),
    path('user', views.users_view,name='user'),
]