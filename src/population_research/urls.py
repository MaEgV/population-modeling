from django.urls import path
from. import views

urlpatterns = [
    path("research/", views.CreateResearch.as_view())
]