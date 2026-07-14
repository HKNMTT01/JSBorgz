from datetime import date
from django.test import TestCase
from accounts.models import User
from .services import working_days
class LeaveTests(TestCase):
    def test_working_days_excludes_weekend(self):
        self.assertEqual(working_days(date(2026,7,13),date(2026,7,19)),5)
