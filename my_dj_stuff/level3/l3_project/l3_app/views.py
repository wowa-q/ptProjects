
from django.shortcuts import render
from . import forms


# Create your views here.

def index(request):
    return render(request, 'l3_app/index.html')

def form_name_view(request):
    form = forms.FormName()
    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            # do something here:
            print('Validation successfuly')
            print("Name: " + form.cleaned_data['name'])
            print("Email: " + form.cleaned_data['email'])
            
            print("Txt: " + form.cleaned_data['text'])
    return render(request, 'l3_app/form.html', {'form': form})

def users_view(request):
    form = forms.UserInputForm()
    if request.method == 'POST':
        form = forms.UserInputForm(request.POST)
        if form.is_valid():
        # do something here:
            print('Validation successfuly')

            form.save(commit=True)
            return index(request)
        else:
            print('!!! Error on Input !!!')


    return render(request, 'l3_app/user.html', {'form': form})