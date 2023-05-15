
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


   
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        
class ProfileWithoutImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'city', 'zone', 'contact_no', 'tole']
        widgets= {
            'bio': forms.Textarea(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'zone': forms.TextInput(attrs={'class':'form-control'}),
            'contact_no': forms.TextInput(attrs={'class':'form-control'}),
            'tole': forms.TextInput(attrs={'class':'form-control'}),
        }