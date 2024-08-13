from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app1.views import IndexView, SchoolListView, SchoolDetailView

class App1UrlTest(SimpleTestCase):

    def test_index_url_is_resolved(self):
        ''' test if the right view is used for the given url
        '''
        url = reverse('index')
        # useful to get the output for testing
        # print(resolve(url))
        # ResolverMatch(func=app1.views.IndexView, args=(), kwargs={}, url_name=index, app_names=[], namespaces=[], route=)
        self.assertEquals(resolve(url).func.view_class, IndexView)

    #  path('schools/', views.SchoolListView.as_view(),name='list'),
    def test_school_list_is_resolved(self):
        '''test if the school list url is correctly resolved'''
        url = reverse('app1:list')
        self.assertEquals(resolve(url).func.view_class, SchoolListView)
    
    def test_school_detail_is_resolved(self):
        '''test if school/<int:pk> url is correctly resolved'''
        url = reverse('app1:school_detail', args=[200000])   # irgendein integer für pk
        self.assertEquals(resolve(url).func.view_class, SchoolDetailView)