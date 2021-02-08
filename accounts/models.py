from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models


class User(PermissionsMixin, AbstractBaseUser):
	first_name = models.CharField(
		verbose_name='Imię',
		max_length=150,
		blank=True
	)
	last_name = models.CharField(
		verbose_name='Nazwisko',
		max_length=150,
		blank=True
	)
	email = models.EmailField(verbose_name='Adres email', blank=True)
	is_staff = models.BooleanField(
		verbose_name='Czy w personelu?',
		default=False,
		help_text='Designates whether the user can log into this admin site.')
	is_active = models.BooleanField(
		verbose_name='Czy aktywny',
		default=True,
		help_text='Designates whether this user should be treated as active. '
		'Unselect this instead of deleting accounts.'
	)
	date_joined = models.DateTimeField(
		verbose_name='Data dołączenia',
		auto_now_add=True
	)

	# TODO change manager
	# objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = 'Użytkownik'
		verbose_name_plural = 'Użytkownicy'

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
		full_name = f'{self.first_name} {self.last_name}'
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)


class Customer(User):
	pass


class Administrator(User):
	pass
