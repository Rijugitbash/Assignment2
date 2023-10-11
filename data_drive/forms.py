from django import forms
from .models import Folder, File

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder_name']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file']
