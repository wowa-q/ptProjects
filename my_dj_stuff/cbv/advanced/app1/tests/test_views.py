from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
import json
from app1.views import IndexView, SchoolListView, SchoolDetailView
from app1.models import School, Student

class App1ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.schools_url = reverse('app1:list')
        self.schools_create_url = reverse('app1:create') 
        

    def test_index_GET(self):
        ''' test if the right view is used for the given url
        '''
        
        response = self.client.get(self.index_url)
        # test the positive response code first
        self.assertEquals(response.status_code, 200)
        # test that the right template was used
        self.assertTemplateUsed(response, 'index.html')

    def test_schools_GET(self):
        ''' test if the right view is used for the given url
        '''
        
        response = self.client.get(self.schools_url)
        # test the positive response code first
        self.assertEquals(response.status_code, 200)
        # test that the right template was used
        self.assertTemplateUsed(response, 'app1/schools.html')

    def test_school_detail_GET(self):
        ''' test if the right view is used for the given url and corect reaction on the GET request
        '''
        schools_detail_url = reverse('app1:school_detail', args=[0])
        response = self.client.get(schools_detail_url)
        # test the negative response code first, because no school was created yet
        self.assertEquals(response.status_code, 404)

        # create a schols object
        school1 = School.objects.create(name='Lessing',
                              principal='Director',
                              location='Wenden')
        # calculate new url with pk from the created object
        schools_detail_url = reverse('app1:school_detail', args=[school1.pk])
        response = self.client.get(schools_detail_url)
        # test the positive response code first
        self.assertEquals(response.status_code, 200)
        # test that the right template was used
        self.assertTemplateUsed(response, 'app1/school_detail.html')

    def test_school_POST_add_school(self):
        ''' test if the right view is used for the POST request
        '''
        # create a schols object
        school1 = School.objects.create(name='Lessing',
                              principal='Director',
                              location='Wenden')

        response = self.client.post(self.schools_create_url)
        
        # test the positive response code first
        self.assertEquals(response.status_code, 200)
        # test that the right template was used
        self.assertTemplateUsed(response, 'app1/school_form.html')
        # test that new object was added
        self.assertEquals(school1.name, 'Lessing')

    def test_school_POST_no_data(self):
        ''' test if the right view is used for the POST request
        '''
        

        response = self.client.post(self.schools_create_url)
        
        # test the positive response code first
        self.assertEquals(response.status_code, 200)
        # test that the right template was used
        self.assertTemplateUsed(response, 'app1/school_form.html')