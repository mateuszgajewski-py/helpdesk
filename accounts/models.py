from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager as Manager
from django.core.mail import send_mail
from django.db import models


class UserManager(Manager):
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        email = self.normalize_email(email)
        customer = Customer(email=email, **extra_fields)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        email = self.normalize_email(email)
        admin = Administrator(email=email, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin


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
    email = models.EmailField(verbose_name='Adres email', unique=True)
    is_staff = models.BooleanField(
        verbose_name='Czy w personelu?',
        default=False,
        help_text='Sprawdza czy użytkownik może zobaczyć część '
                  'administracyjną')
    is_active = models.BooleanField(
        verbose_name='Czy aktywny',
        default=True,
        help_text='Sprawdza czy użytkownik jest aktywny. Odznacz zamiast '
                  'usuwania konta bądź w przypadku blokady'
    )
    date_joined = models.DateTimeField(
        verbose_name='Data dołączenia',
        auto_now_add=True
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

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
    class Meta:
        verbose_name = 'Klient'
        verbose_name_plural = 'Klienci'


class Administrator(User):
    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administratorzy'
