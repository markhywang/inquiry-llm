from django.urls import path

from . import views

urlpatterns = [
    # Web routes
    path("", views.index, name="index"),
    
    # API routes
    path("generate", views.generate, name="generate")
]