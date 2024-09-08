from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("products.urls")),
    path("", include("users.urls")),
    path("api/stripe/", include("payments.urls")),
]