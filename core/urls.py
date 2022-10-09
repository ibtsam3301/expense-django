from django.urls import path
from . import views



urlpatterns = [
    path("", views.homepage, name="generate-bill"),
    path("download-pdf/<year>/<month>", views.generate_PDF, name="download-pdf"),
 
]