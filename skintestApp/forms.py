from django import forms
from .models import Image, Feedback
class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']

# forms.py
from django import forms

class QueryForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    query = forms.CharField(widget=forms.Textarea)
