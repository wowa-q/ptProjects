
# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy

from . import models

# Create your views here.
# def index(request):
#     return render(request, 'index.html')


class IndexView(TemplateView):
    
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = 'BASIC INJECTIONS'
        return context

class SchoolListView(ListView):
    model = models.School
    # returns a context modelname_list -> school_list and it can be used in the templates
    # better however is to define own name:
    context_object_name = 'schools'
    template_name = 'app1/schools.html'

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model= models.School
    template_name = 'app1/school_detail.html'

class SchoolCreateView(CreateView):
    model = models.School
    fields = ('name', 'principal', 'location')

class SchoollUpdateView(UpdateView):
    fields = ('name', 'principal')
    model=models.School

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"Updating school with pk: {obj.pk}")  # Debugging-Zeile
        return obj
    
class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy('app1:list')