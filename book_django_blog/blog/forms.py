from django import forms

from blog.models import Comment


class SearchForm(forms.Form):
    query = forms.CharField()


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=32)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, max_length=256, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'name', 'email', 'body',
        )

    def save_comment(self, post):
        new_comment = self.save(commit=False)
        new_comment.post = post
        new_comment.save()
        return new_comment
