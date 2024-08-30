from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="Blog API Docs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)
api_docs_urls = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

api_endpoints = [
    path('posts/', include("posts.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(api_endpoints))
]

if settings.DEBUG:
    urlpatterns += api_docs_urls
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
