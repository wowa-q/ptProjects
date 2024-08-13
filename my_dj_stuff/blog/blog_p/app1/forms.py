from django import forms
from django.contrib.auth.models import User
from app1.models import Comments, Post


class PostForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
        widget = {
            'title':forms.TextInput(attrs={
                'class':'textinputclass'    # textinputclass is the own class to be used in the css
            }),
            'text':forms.Textarea(attrs={
                'class':'editable medium-editor-textarea postcontent' # postcontent is the own class, other come from bootstrap
            })
        }

class CommentForm(forms.ModelForm):
    
    class Meta():
        model = Comments
        fields = ('author', 'text')
        widget = {
            'author':forms.TextInput(attrs={
                'class':'textinputclass'    # textinputclass is the own class to be used in the css
            }),
            'text':forms.Textarea(attrs={
                'class':'editable medium-editor-textarea' # no own classes here, other come from bootstrap
            })
        }

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta():
#         model = User
#         fields = ('username', 'email', 'password' )

# class UserProfileInfoForm(forms.ModelForm):
#     portfolio = forms.URLField(required=False)
#     picture = forms.ImageField(required=False)    

#     class Meta():
#         model = UserProfileInfo
#         fields = ('portfolio', 'picture')