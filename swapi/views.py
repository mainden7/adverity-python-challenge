from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import FilesCollection


class IndexView(ListView):
    template_name = "swapi/index.html"
    queryset = FilesCollection.objects.order_by("-created_at")
    context_object_name = "collections"
