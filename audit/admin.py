from django.contrib import admin
from .models import *
for model in list(globals().values()):
    try:
        if isinstance(model,type) and hasattr(model,'_meta') and model._meta.app_label=='audit': admin.site.register(model)
    except admin.sites.AlreadyRegistered: pass
