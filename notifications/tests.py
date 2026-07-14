from django.test import TestCase
from accounts.models import User
from .services import notify
class NotificationTest(TestCase):
    def test_notify(self):
        u=User.objects.create_user(username='u',email='u@example.com',full_name='U',password='StrongPass123!')
        notify(u,'Test','Message')
        self.assertEqual(u.notifications.count(),1)
