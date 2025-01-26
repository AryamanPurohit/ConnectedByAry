from django.forms import ModelForm
from .models import Project, Review
from django import forms
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link','source_link','image']
        
        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args,**kwargs):
        super(ProjectForm, self).__init__(*args,**kwargs)

        for k,v in self.fields.items():
            v.widget.attrs.update({'class' : 'input'})

        self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder':'Add Title'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Vote Now!',
            'body': 'Your Thoughts.....' 
        }


    def __init__(self, *args,**kwargs):
        super(ReviewForm, self).__init__(*args,**kwargs)

        for k,v in self.fields.items():
            v.widget.attrs.update({'class' : 'input'})

