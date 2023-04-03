from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import FilesCollection
from .services import SWAPIDataAPICollector, SWAPIDataCSVReader

DEFAULT_HEADERS = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld_name",
    "date",
]


class IndexView(ListView):
    template_name = "swapi/index.html"
    queryset = FilesCollection.objects.order_by("-created_at")
    context_object_name = "collections"


class FetchView(View):
    def get(self, request, *args, **kwargs):
        """Fetches new collection and redirects to index page"""
        # TODO: Move data load functionality to background, i.e. use celery
        SWAPIDataAPICollector().collect_all()
        return redirect(reverse("index"))


class BrowseCollectionView(View):
    def get(self, request, collection_id):
        collection = get_object_or_404(FilesCollection, pk=collection_id)
        limit = int(request.GET.get("limit", 10))
        data = SWAPIDataCSVReader().load_data(
            collection.file.name, headers=DEFAULT_HEADERS, start=0, limit=limit
        )
        more_url = (
            f"{request.path}?limit={limit+10}" if limit <= len(data) else None
        )
        context = {
            "headers": DEFAULT_HEADERS,
            "data": data.dicts(),
            "more_url": more_url,
        }
        return render(request, "swapi/collection.html", context)


class ValueCountView(View):
    def get(self, request, collection_id):
        context = {
            "columns": DEFAULT_HEADERS,
            "selected_columns": [],
        }
        return render(request, "swapi/value_count.html", context)

    def post(self, request, collection_id):
        selected_columns = request.POST.getlist("columns")
        collection = get_object_or_404(FilesCollection, pk=collection_id)
        data = SWAPIDataCSVReader().get_value_count(
            collection.file.name,
            headers=DEFAULT_HEADERS,
            columns=selected_columns,
        )
        # import pdb;pdb.set_trace()
        context = {
            "headers": data.header(),
            "columns": DEFAULT_HEADERS,
            "selected_columns": selected_columns,
            "data": data.dicts(),
        }
        return render(request, "swapi/value_count.html", context)
