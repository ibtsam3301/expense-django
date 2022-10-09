from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("", csrf_exempt(views.homepage), name="generate-bill"),
    path("download-pdf/<year>/<month>", csrf_exempt(views.generate_PDF), name="download-pdf"),
 
]