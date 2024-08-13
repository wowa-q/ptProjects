from django.urls import path

from app1 import views

app_name = 'app1' # app1 wird dann in den Templates genutzt

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', views.PostDetailView.as_view(),name='post_detail'),    
    path('post/<int:pk>/edit', views.PostUpdateView.as_view(),name='post_edit'),
    path('post/<int:pk>/del', views.PostDeleteView.as_view(),name='post_del'),
    path('drafts', views.DraftListView.as_view(),name='drafts'),
    path('post/<int:pk>/comment', views.add_comment_to_post,name='add_comment_to_post'),
    path('post/<int:pk>/approve', views.comment_approve,name='comment_approve'),
    path('post/<int:pk>/remove', views.comment_remove,name='comment_remove'),
    path('post/<int:pk>/publish', views.post_publish,name='post_publish'),
    
]