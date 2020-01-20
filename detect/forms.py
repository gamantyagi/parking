from django import forms


class ImageObForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(max_length=200)
