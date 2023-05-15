from django import forms  
from django.forms import ModelForm
from .models import Pdf_Info


class BookForm(ModelForm):
    class Meta:
        model = Pdf_Info
        fields = '__all__' # this covers all the data of the product class in models