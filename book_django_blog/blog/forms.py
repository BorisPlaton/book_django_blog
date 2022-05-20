from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=32)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, max_length=256, widget=forms.Textarea)
