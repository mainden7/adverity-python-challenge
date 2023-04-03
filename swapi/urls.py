from django.urls import path

from .views import IndexView
from .views import FetchView
from .views import BrowseCollectionView
from .views import ValueCountView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("fetch", FetchView.as_view(), name="fetch"),
    path(
        "collections/<int:collection_id>",
        BrowseCollectionView.as_view(),
        name="browse_collection",
    ),
    path(
        "collections/<int:collection_id>/value_count",
        ValueCountView.as_view(),
        name="value_count",
    ),
]
