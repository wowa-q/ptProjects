from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import index

class MyTest(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        # ResolverMatch(func=app1.views.IndexView, args=(), kwargs={}, url_name=index, app_names=[], namespaces=[], route=)
        self.assertEquals(resolve(url).func, index)