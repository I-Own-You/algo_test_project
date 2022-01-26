from enum import unique
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django import forms
from .models import User


class UserRegisterForm(forms.Form):

    first_name = forms.CharField(label='Имя', max_length=15, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=15, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    email = forms.EmailField(label='E-mail', required=True, error_messages={'invalid':"Введите правильный e-mail адрес"})
    password = forms.CharField(label='Пароль', max_length=20, widget=forms.TextInput(
        attrs=({'type': 'password'})), required=True)
    password_repeat = forms.CharField(
        label='Повторите пароль', max_length=20, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Введите повторно пароль', 'type': 'password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.fields[key].widget.attrs.update({
            'class': 'form-inp'
        }) for key in self.fields]

        [self.fields[key].widget.attrs.update({
            'placeholder': f'Введите {self.fields[key].label}'
        }) for key in self.fields if self.fields[key].label not in ('Повторите пароль Фамилия')]

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name.isalpha():
            raise ValidationError('Имя должно содержать только буквы')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name.lower().isalpha():
            raise ValidationError('Фамилия должна содержать только буквы')

        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('E-mail уже был использован')
        else:
            validate_email(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password.isalnum() or len(password) < 10:
            raise ValidationError(
                'Пароль должен содержать от 10 до 15 символов включая только буквы и цифры')

        return password

    def clean_password_repeat(self):
        password_repeat = self.cleaned_data.get('password_repeat')
        password = self.cleaned_data.get('password')

        if password_repeat != password:
            raise ValidationError(
                'Пароли не совпадает')

        return password_repeat
