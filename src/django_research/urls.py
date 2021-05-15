from django.urls import path
from. import views

urlpatterns = [
    path(r'researcher/<str:id>/', views.CreateResearch.as_view()),  # Load population from DB
    path(r'researcher/', views.CreateResearch.as_view()),  # Create new population
    path(r'researcher/<str:token>/run/', views.ResearchRun.as_view()),  # Run researcher with parameters(POST)
    path(r'researcher/<str:token>/add/', views.ResearchAddIndividual.as_view())  # Add individual to population(POST)
]
