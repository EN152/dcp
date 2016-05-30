# -*- coding: utf-8 -*-

# Fehler beim import in Travis und ich weiﬂ nicht warum
from django.contrib.auth.models import User

u, created = User.objects.get_or_create(username='admin')
if created:
    u.set_password('password')
    u.is_superuser = True
    u.is_staff = True
    u.save()
else:
    u.set_password('password')