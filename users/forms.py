from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core import validators
from django.forms import ModelForm

from users.models import User, OneTimeCode


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}), validators=[validators.MinLengthValidator(2)],
        error_messages={'min_length': 'Длина имени меньше 2 знаков'})
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}), validators=[validators.MinLengthValidator(2)],
        error_messages={'min_length': 'Длина фамилии меньше 2 знаков'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class CodeForm(ModelForm):
    """Форма для ввода кода при регистрации"""
    class Meta:
        model = OneTimeCode
        fields = ['code']
