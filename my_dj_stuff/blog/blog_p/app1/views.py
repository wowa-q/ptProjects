from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)



from app1.models import Post, Comments
from app1.forms import PostForm, CommentForm

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    redirect_field_name = 'app1/post_list.html'
    # SQL query from django
    def get_queryset(self) -> QuerySet[Any]:
        # __lte: SQL query less that or equal to (https://docs.djangoproject.com/en/5.1/topics/db/queries/)
        # '-published_date' - bewirkt, dass der neuste Blog oben sein wird
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post
    template_name = 'app1/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin 
    login_url = '/login/'
    redirect_field_name = 'app1/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Den Post speichern, aber noch nicht in die Datenbank schreiben
        post = form.save(commit=False)
        post.author = self.request.user  # Den aktuellen Benutzer als Autor setzen
        post.save()  # Post speichern

        # Nach dem Speichern zur Detailansicht des Posts weiterleiten
        return redirect('app1:post_detail', pk=post.pk)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'app1/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        # Den Post speichern, aber noch nicht in die Datenbank schreiben
        post = form.save(commit=False)
        post.author = self.request.user  # Den aktuellen Benutzer als Autor setzen
        post.save()  # Post speichern

        # Nach dem Speichern zur Detailansicht des Posts weiterleiten
        return redirect('app1:post_detail', pk=post.pk)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    # login_url = '/login/'
    success_url = reverse_lazy('app1:post_list') # reverse_lazy nutzt man um URL zu berechnen
    
    model = Post

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'app1/post_list.html'

    model = Post

    def get_queryset(self) -> QuerySet[Any]:

        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

###########################################################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('app1:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'app1/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('app1:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk = comment.post.pk
    comment.delete()    
    return redirect('app1:post_detail', pk=post_pk) # comment.post.pk da comment gelöscht wurde

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('app1:post_detail', pk=pk) 

