from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# from apps.core.forms.user import UserForm
from apps.core.models import User_Profile
from django.utils.log import getLogger

log = getLogger('django')




class UserSettingsForm(forms.Form):

    error_messages = {
        'duplicate_email' : _('A user with that email already exists.'),
    }

    email = forms.EmailField(label=_('email'),
                             widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
                             help_text=_(''),
                             required=False)

    nickname = forms.CharField(label=_('nickname'),
                               widget=forms.TextInput(attrs={'class':'form-control'}),
                               help_text=_(''))

    location = forms.CharField(
        widget=forms.Select(attrs={"name" : "location", "class" : "form-control location"}),
        label=_('location'),
        required=False
    )

    city = forms.CharField(
        widget=forms.Select(attrs={'name' : 'city', 'class' : 'form-control city'}),
        label=_('city'),
        required=False
    )

    gender = forms.ChoiceField(label=_('gender'),
                                choices=User_Profile.GENDER_CHOICES,
                                # widget=forms.Select(attrs={'class':'form-control'}),
                                widget=forms.Select(attrs={'class':'form-control'}),
                                help_text=_(''))
    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'class':'form-control','rows':'4', 'style':'resize:none;'}),
                          required=False,
                          max_length=200,
                          help_text=_(''))
    website = forms.URLField(label=_('website'),
                             widget=forms.URLInput(attrs={'class':'form-control'}),
                             required=False,
                             help_text=_(''))


    def clean_email(self):
        _email = self.cleaned_data.get('email')

        if self.user_cache.email == _email:
            return _email

        try:
            get_user_model()._default_manager.get(email = _email)
        except get_user_model().DoesNotExist:
            return _email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code= 'duplicate_email',
        )
        # return _email

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserSettingsForm, self).__init__(*args, **kwargs)

    def save(self):
        _nickname = self.cleaned_data.get('nickname', None)
        _location = self.cleaned_data.get('location', None)
        _city = self.cleaned_data.get('city', None)
        _gender = self.cleaned_data.get('gender', None)
        _bio = self.cleaned_data.get('bio', None)
        _website = self.cleaned_data.get('website', None)

        self.user_cache.profile.nickname = _nickname
        self.user_cache.profile.location = _location
        self.user_cache.profile.city = _city
        self.user_cache.profile.gender = _gender
        self.user_cache.profile.bio = _bio
        self.user_cache.profile.website = _website

        self.user_cache.profile.save()


class UserChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    current_password = forms.CharField(
        label=_('current password'),
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    new_password = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        min_length=8,
    )

    password_confirmation = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        min_length=8,
    )


    def clean_current_password(self):
        _current_password = self.cleaned_data.get('current_password')
        if self.user_cache.check_password(_current_password):
            return _current_password
        else:
            raise forms.ValidationError(
                'password error'
            )

    def clean_password_confirmation(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('password_confirmation')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def __init__(self, user, *args, **kwargs):
        self.user_cache = user
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def save(self):
        # log.info(self.cleaned_data)
        _password = self.cleaned_data.get('password_confirmation')
        self.user_cache.set_password(_password)
        self.user_cache.save()

__author__ = 'edison'
