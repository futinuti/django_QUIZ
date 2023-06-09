from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.shortcuts import get_object_or_404

from .apps import user_register


class UserRepeatSend(forms.ModelForm):
    email = forms.EmailField(label='email')

    def save(self, commit=True):
        # email = super().save(commit=False)
        email = self.cleaned_data['email']
        user = get_object_or_404(get_user_model(), email=email)

        if commit:
            user.save()

        user_register.send(get_user_model(), instance=user)

        return user

    class Meta:
        model = get_user_model()
        fields = (
            'email',
        )


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='email')
    password1 = forms.CharField(
        label='password',  # определяет название
        widget=forms.PasswordInput,  # виджет для скрытия символов
        help_text=password_validation.password_validators_help_text_html  # стандартный джанговские правила для пароля
    )
    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput,
        help_text='please repeat password'
    )

    def clean_password1(self):
        """ навешивается на перое поле для проверки соответствия правилам паролей """
        pwd = self.cleaned_data['password1']
        if pwd:
            password_validation.validate_password(pwd)
        return pwd

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError(
                {
                    'password2': ValidationError('Password not equals', code='password_mismatch')
                }
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # шифруем пароль
        user.is_activated = False  # сбрасываем флаги чтоб пользователь не смог залогиниться после регистрации
        user.is_active = False

        if commit:
            user.save()

        user_register.send(get_user_model(), instance=user)

        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class UserUpdateForm(UserChangeForm):
    avatar = forms.ImageField(required=False, widget=widgets.FileInput())
    birthday = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'city',
            'avatar'
        )

        # widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})}
