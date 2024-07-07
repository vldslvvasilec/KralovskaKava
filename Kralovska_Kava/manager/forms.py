from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from modeltranslation.forms import TranslationModelForm
from django.conf import settings
from home.models import Category, Product
from .models import Manager

class ManagerLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your login')}),
        label=_("Login")
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter your password')}),
        label=_("Password")
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not Manager.objects.filter(username=username).exists():
            raise forms.ValidationError(_("The user with this login does not exist"))
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(_("Invalid username or password"))
        return cleaned_data





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['background_css', 'is_active']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for lang_code, lang_name in settings.LANGUAGES:
            self.fields[f'name_{lang_code}'] = forms.CharField(label=f'{_("Name")} ({lang_name})', required=False,
                                                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        instance = super(CategoryForm, self).save(commit=False)
        for lang_code, _ in settings.LANGUAGES:
            setattr(instance, f'name_{lang_code}', self.cleaned_data[f'name_{lang_code}'])
        if commit:
            instance.save()
        return instance


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'category', 'description', 'components', 'is_active']
