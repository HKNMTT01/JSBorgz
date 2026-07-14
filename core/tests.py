from django.test import TestCase
from django.urls import reverse
from accounts.models import User,Department
class CoreFlowTests(TestCase):
    def setUp(self):
        d=Department.objects.create(name='IT')
        self.user=User.objects.create_user(username='amira@example.com',email='amira@example.com',password='StrongPass123!',full_name='Amira',department=d)
    def test_login_and_dashboard(self):
        self.assertTrue(self.client.login(email='amira@example.com',password='StrongPass123!'))
        response=self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Amira')
    def test_health(self):
        response=self.client.get(reverse('health'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['database'],1)
