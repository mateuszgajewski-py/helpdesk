import os

from django.conf import settings
from django.test import TestCase

from accounts import models as am
from helpdesk_app import models


def get_test_file():
	with open(os.path.join(settings.BASE_DIR + '.gitignore')) as file:
		return file


class TicketTest(TestCase):
	def setUp(self) -> None:
		self.client_user = am.User.objects.create_user(
			email='example@example.com',
			password='Pass!234'
		)
		self.category = models.Category.objects.create(
			name='test',
			slug='test',
			is_visible=True
		)
		self.ticket = models.Ticket.objects.create(
			author=self.client_user,
			category=self.category,
			title='Example Ticket',
			description='Example',
		)
		self.comment = models.TicketComment.objects.create(
			ticket=self.ticket,
			comment='Example',
		)
		self.file = models.TicketFile.objects.create(
			ticket=self.ticket,
			file=get_test_file(),
		)

	def test_str(self):
		self.assertEqual(self.ticket, self.ticket.title)