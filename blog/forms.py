from django import forms
from .models import Post, CVEntry


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
        )


class DateInput(forms.DateInput):
    input_type = 'date'


class CVEntryForm(forms.ModelForm):
    class Meta:
        model = CVEntry
        fields = ('section', 'text', 'start_date', 'end_date')
        widgets = {'start_date': DateInput(), 'end_date': DateInput()}
