from django.urls import path

from .views import IndexView
from .views import FetchView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("fetch", FetchView.as_view(), name="fetch"),
    # path(
    #     "collections/<int:collection_id>/browse",
    #     views.browse_collection,
    #     name="browse_collection",
    # ),
    # path(
    #     "collections/<int:collection_id>/value_count",
    #     views.value_count_collection,
    #     name="value_count_collection",
    # ),
]