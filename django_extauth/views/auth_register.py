from django import forms
from django.contrib.auth import password_validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

from django_sendmail import send_mail

from ..models import ExternalIdentity, create_user
from .auth_links import finish_registration_by_email_link, login_link, password_reset_link


class AuthRegisterForm(forms.Form):
	email = forms.EmailField(label=_("Email"), max_length=254, required=True)
	password = forms.CharField(
		label=_("Password"),
		strip=False,
		widget=forms.PasswordInput,
		help_text=password_validation.password_validators_help_text_html(),
	)

	given_name = forms.CharField(label=_("Given name"), required=False)
	family_name = forms.CharField(label=_("Family name"), required=False)

	state = forms.CharField(widget=forms.HiddenInput, required=False)

	def process(self, request):
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']

		profile_data = dict(
			given_name = self.cleaned_data['given_name'],
			family_name = self.cleaned_data['family_name'],
		)

		site = get_current_site(request)

		query = {}
		if self.cleaned_data['state']:
			query['state'] = self.cleaned_data['state']

		try:
			ei = ExternalIdentity.objects.get(email=email)
		except ExternalIdentity.DoesNotExist:
			username, domain = email.split('@', 1)
			user = create_user(username)
			user.set_password(password)
			for k, v in profile_data.items():
				setattr(user, k, v)
			user.save()

			confirm_email = finish_registration_by_email_link(site, email, user, **query)
			if request.flow:
				confirm_email += '?flow=' + request.flow.id

			send_mail(email, 'registration/email/welcome', {
				'user': user,
				'email': email,
				'confirm_email': confirm_email,
			}, request=request)
			# Note: We can't log in here, as we can't log in in the 'else' case,
			# and it would tell the attacker if this e-mail is in the database
		else:

			if ei.trusted:
				reset_password = password_reset_link(site, ei.email, ei.user, **query)
				log_in = login_link(ei.email)
				if request.flow:
					reset_password += '?flow=' + request.flow.id
					log_in += '?flow=' + request.flow.id

				send_mail(ei.email, 'registration/email/welcome-back', {
					'user': ei.user,
					'reset_password': reset_password,
					'log_in': log_in,
				}, request=request)
			else:
				send_mail(ei.email, 'registration/email/welcome-back', {
					'user': ei.user,
				}, request=request)

		return _("Check your e-mail.")
