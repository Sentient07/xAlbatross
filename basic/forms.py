__author__ = 'ramana'

from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    mobile_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'mobile_number')

    # clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email or username')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=30,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Email',
                                   'class': 'form-control'}),
                               required=True,
                               error_messages={
                                   'required': 'Please enter an EmailID.'})
    password = forms.CharField(label=("Password"),
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Password'}),
                               required=True,
                               error_messages={
                                   'required': 'Please enter a password.'})

    error_messages = {
        'invalid_login': ("Please enter a correct %(EmailId)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': ("This account is inactive."),
    }
