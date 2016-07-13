# -*- coding: utf-8 -*-
from django.views.generic import View
from django.views.generic import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from django.utils.http import urlencode
from braces import views
from dcp.models import *
from django.template import loader
from dcp.forms import *
from .models import Message
from .models import Catastrophe
from .forms import *
from django.core.urlresolvers import reverse,reverse_lazy
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseForbidden
