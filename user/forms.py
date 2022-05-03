from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_resized import ResizedImageField


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={"class": "form-control color"}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={"class": "form-control color"}))
    company = forms.CharField(label="Company", widget=forms.TextInput(
        attrs={"class": "form-control color"}))
    email = forms.EmailField(label="Email Address", max_length=254, help_text='Email.',widget=forms.TextInput(
        attrs={"class": "form-control color"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"class": "form-control color"}))
    password2 = None
    accept = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'company', 'email', 'password1', 'accept')


class LoginForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", max_length=254, help_text='Email.',widget=forms.TextInput(
        attrs={"class": "form-control color"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"class": "form-control color"}))
    password2 = None

    class Meta:
        model = Profile
        fields = ('email', 'password1')
        
import unicodedata
from user.models import Profile
from django.template import loader
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def clean_email(self):
        try:
            Profile.objects.get(email=self.data.get('email'))
            return self.data.get('email')
        except Profile.DoesNotExist:
            raise forms.ValidationError('Email does not exists!')

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email = EmailMessage(
            subject,
            body,
            from_email,
            [to_email]
        )
        email.content_subtype = "html"
        email.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = Profile.get_email_field_name()
        active_users = Profile.objects.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = Profile.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )