from django import forms
from .models import TextFile

# Create a form for uploading text files
class TextFileForm(forms.ModelForm):
    class Meta:
        model = TextFile
        fields = ['file']



class PromptForm(forms.Form):
    temperature = forms.FloatField(min_value=0.0, max_value=1.0, initial=0.7, label="Temperature")
    top_p = forms.FloatField(min_value=0.0, max_value=1.0, initial=1.0, label="Top_p")