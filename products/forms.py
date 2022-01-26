from dataclasses import fields
from distutils.command.upload import upload
from django.core.exceptions import ValidationError
from django import forms
from .models import  Car, Images
from django.forms.models import inlineformset_factory
import re


#

class ImageForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ['images']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),
        }


class AddEditProductForm(forms.Form):
    name = forms.CharField(label='Имя машины', max_length=20, widget=forms.TextInput(
        attrs=({'placeholder': 'Введите имя машины'})), required=True)
    description = forms.CharField(
        label='Описание машины', max_length=300, widget=forms.Textarea(attrs=({
            'rows': '7', 'cols': '50', 'placeholder': 'Введите описание машины'})), required=True)
    price = forms.IntegerField(label='Цена машины', widget=forms.TextInput(
        attrs=({'placeholder': 'Введите цену машины'})), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update({
            'class': 'form-inp'
        }) for key in self.fields]

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not re.match('[A-Za-z0-9 ]+$', name):
            raise ValidationError('Имя машины должно содержать только буквы и цифры')

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if type(price) != int:
            raise ValidationError(
                'Цена машины должна быть обозначана в целых числах')

        return price


CarImageFormSet = inlineformset_factory(
    Car, Images, form=ImageForm,
    extra=1, can_delete=True, #fields=['images'],
)