from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import FilesCollection
from .services import SWAPIDataCollector


class IndexView(ListView):
    template_name = "swapi/index.html"
    queryset = FilesCollection.objects.order_by("-created_at")
    context_object_name = "collections"


class FetchView(View):
    def get(self, request, *args, **kwargs):
        """Fetches new collection and redirects to index page"""
        # TODO: Move data load functionality to background, i.e. use celery
        SWAPIDataCollector().collect_all()
        return redirect(reverse("index"))
