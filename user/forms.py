from django.contrib.auth.forms import UserCreationForm

from user.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telegram_id')

    user_type = forms.ChoiceField(choices=(('1', 'Волонтёр'),
                                           ('2', 'Работодатель')))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
