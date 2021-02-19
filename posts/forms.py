from django import forms
from .models import Post, Comment

class Create_Post_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']
    
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'row':10}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        