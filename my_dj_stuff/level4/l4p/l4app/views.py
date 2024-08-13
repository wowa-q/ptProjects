from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'l4app/index.html')

def relative(request):
    return render(request, 'l4app/relative.html')

def users_view(request):
    return render(request, 'l4app/user.html')