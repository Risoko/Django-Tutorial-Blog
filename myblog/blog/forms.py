from django import forms
from django.core.mail import send_mail

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25
    )
    to = forms.EmailField()
    email = forms.CharField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, post=None, request=None, *args, **kwargs):
        if post and request:
            self.post = post
            self.request = request
        super().__init__(*args, **kwargs)

    def save(self):
        post_u = self.request.build_absolute_uri(self.post.get_absolute_url())
        post_title = self.post.title
        name = self.cleaned_data['name']
        subject = f"{name} recommends you reading {post_title}"
        message = f"Read {post_title} at {post_u}\n\n \
        {name}\'s comments: {self.cleaned_data['comments']}"
        send_mail(subject, message, 'admin@myblog.com', [self.cleaned_data['to']])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

    def __init__(self, post=None, *args, **kwargs):
        if post:
            self.post = post
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        new_comment = super().save(commit=False)
        new_comment.post = self.post
        if commit:
            new_comment.save()
            return
        return new_comment


class SearchForm(forms.Form):
    query = forms.CharField()
        