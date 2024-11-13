from django import forms
from .models import TextFile

# Create a form for uploading text files
class TextFileForm(forms.ModelForm):
    class Meta:
        model = TextFile
        fields = ['file']

# Create a separate form for the user to input the prompt they want to send to OpenAI
class PromptForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), label="Prompt for OpenAI")