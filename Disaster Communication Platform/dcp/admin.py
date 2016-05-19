from django.contrib import admin

# Register models here.

from .models import Catastrophe

admin.site.register(Catastrophe)