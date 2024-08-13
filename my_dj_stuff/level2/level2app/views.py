from django.shortcuts import render
from django.http import HttpResponse
from level2app.models import Topic, AccessRecord, Webpage
# Create your views here.

def index(request):
    webpages_list = AccessRecord.objects.order_by('date')
    date_dict = {'acess_record': webpages_list}
    return render(request, 'level2app/index.html', context=date_dict)
# Create your views here.
