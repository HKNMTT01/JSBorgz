import os, secrets
from django.core.management.base import BaseCommand
from accounts.models import User,Department
class Command(BaseCommand):
    help='Create or reset the initial HR administrator.'
    def add_arguments(self,p):
        p.add_argument('--email',default=os.getenv('BOOTSTRAP_ADMIN_EMAIL','admin@jetama.local'))
        p.add_argument('--password',default=os.getenv('BOOTSTRAP_ADMIN_PASSWORD'))
        p.add_argument('--name',default='HR Administrator')
    def handle(self,*args,**o):
        password=o['password'] or secrets.token_urlsafe(14)
        dept,_=Department.objects.get_or_create(name='Human Resources & ESG',defaults={'code':'HRESG'})
        user,_=User.objects.get_or_create(email=o['email'].lower(),defaults={'username':o['email'].lower(),'full_name':o['name']})
        user.username=o['email'].lower(); user.full_name=o['name']; user.department=dept; user.role=User.Role.ADMIN; user.is_staff=True; user.is_superuser=True; user.set_password(password); user.save()
        self.stdout.write(self.style.SUCCESS(f'Admin ready: {user.email}'))
        self.stdout.write(f'Password: {password}')
