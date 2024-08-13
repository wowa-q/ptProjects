from django.test import SimpleTestCase
from app1.forms import MyForm

class TestForm(SimpleTestCase):

    def test_myform_valid_data(self):
        form = MyForm(data={
            'title': 'transaction',
            'amount': 100,
        })
        # check if the form data input is valid
        self.assertTrue(form.is_valid())

    def test_myform_invalid_data(self):
        form = MyForm(data={})
        self.assertFalse(form.is_valid())
        # number of errors per missing data pair
        self.assertEquals(len(form.errors), 2)