from django.contrib import admin
from .models import Notice, Policy, Circular
for model in (Notice, Policy, Circular):
    try: admin.site.register(model)
    except admin.sites.AlreadyRegistered: pass
