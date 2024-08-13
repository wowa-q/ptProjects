from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
import json
from app1.views import IndexView, SchoolListView, SchoolDetailView
from app1.models import School, Student

class App1ModelTest(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name = 'NO',
            principal = 'aleuchter',
            location = 'Querum'
        )

    def test_school_is_assigned_pk_on_creation(self):
        self.assertEquals(self.school.pk, 1)