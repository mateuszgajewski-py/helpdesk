from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


class Category(models.Model):
	name = models.CharField(verbose_name='Nazwa', max_length=100)
	slug = models.SlugField(unique=True)
	is_visible = models.BooleanField(
		verbose_name='Czy widoczne?',
		help_text='Określa czy można utworzyć zgłoszenie z taką kategorią'
	)

	class Meta:
		verbose_name = 'Kategoria'
		verbose_name_plural = 'Kategorie'

	def __str__(self):
		return self.name


class Ticket(models.Model):

	class StatusChoices(models.IntegerChoices):
		NEW = 1, 'Nowy'
		MAINTAINER_SET = 2, 'Przypisano Opiekuna'
		IN_PROGRESS = 3, 'W trakcie'
		DONE = 4, 'Zakończono'

	author = models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		verbose_name='Autor',
		on_delete=models.PROTECT
	)
	maintainer = models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		verbose_name='Opiekun',
		on_delete=models.SET_NULL,
		null=True,
		blank=True
	)
	category = models.ForeignKey(
		to=Category,
		verbose_name='Kategoria',
		on_delete=models.PROTECT,
	)
	title = models.CharField(verbose_name='Tytuł', max_length=100)
	description = models.TextField(verbose_name='Opis')
	create_date = models.DateTimeField(
		verbose_name='Data utworzenia',
		auto_now_add=True
	)
	last_update = models.DateTimeField(
		verbose_name='Data ostatniej zmiany',
		auto_now=True
	)
	status = models.IntegerField(
		verbose_name='Status',
		choices=StatusChoices.choices,
		default=StatusChoices.NEW
	)

	class Meta:
		verbose_name = 'Zgłoszenie'
		verbose_name_plural = 'Zgłoszenia'

	def __str__(self):
		return self.title


def file_path(instance, filename):
	return f'ticket_{instance.id}/{filename}'


class TicketFiles(models.Model):
	ticket = models.ForeignKey(
		to=Ticket,
		verbose_name='Zgłoszenie',
		related_name='files',
		on_delete=models.CASCADE
	)
	file_storage = FileSystemStorage(location=settings.FILE_ROOT)
	file = models.FileField(
		verbose_name='Plik',
		storage=file_storage,
		upload_to=file_path
	)
	create_date = models.DateTimeField(
		verbose_name='Data dodania',
		auto_now_add=True
	)

	class Meta:
		verbose_name = 'Załącznik'
		verbose_name_plural = 'Załączniki'

	def __str__(self):
		return self.file.name


class TicketComment(models.Model):
	ticket = models.ForeignKey(
		to=Ticket,
		verbose_name='Zgłoszenie',
		related_name='comments',
		on_delete=models.CASCADE
	)
	author = models.ForeignKey(
		to=settings.AUTH_USER_MODEL,
		verbose_name='Autor',
		on_delete=models.SET_NULL,
		null=True,
		blank=True
	)
	comment = models.CharField(verbose_name='Komentarz', max_length=100)
	create_date = models.DateTimeField(
		verbose_name='Data dodania',
		auto_now_add=True
	)

	class Meta:
		verbose_name = 'Komentarz'
		verbose_name_plural = 'Komentarze'

	def __str__(self):
		return f'Komentarz użytkownika {self.author}'
