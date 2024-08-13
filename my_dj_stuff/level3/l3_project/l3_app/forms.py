
from django import forms
from django.core import validators

from l3_app.models import User


class UserInputForm(forms.ModelForm):

        class Meta:
            model = User
            fields ='__all__'


def check_for_z(value):
    if value[0].lower() != 'z':
        raise forms.ValidationError("Name needs to start with z")

class FormName(forms.Form):
    name = forms.CharField(validators=[check_for_z])
    email = forms.EmailField()
    verify_email = forms.EmailField(label='repeat your email')
    text = forms.CharField(widget=forms.Textarea)
    # this is to catch the bots
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email'] # email is der name des fields
        vemail = all_clean_data['verify_email']
        if email != vemail:
            raise forms.ValidationError('email not the same!')

    """ the function is used if validator is not used
    # pattern: clean_fieldname, here botcatcher
    def clean_botcatcher(self):
        if len(self.botcatcher) > 0:
            raise forms.ValidationError("GOTCHA BOT!")
        return self.botcatcher
    """

