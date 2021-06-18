from django.urls import path  # type: ignore
from. import views

urlpatterns = [
    path(r'research/<int:population_id>/', views.CreateResearch.as_view()),  # Load population from DB
    path(r'research/', views.CreateResearch.as_view()),  # Create new population
    path(r'research/<str:token>/run/', views.ResearchRunner.as_view()),  # Run research with parameters(POST)
    path(r'research/<str:token>/add/', views.IndividualAdder.as_view()),  # Add individual to population(POST)
    path(r'research/<str:token>/delete/', views.PopulationManager.as_view()),  # Delete individual from OM
    path(r'research/<str:token>/save/', views.PopulationManager.as_view()),  # Save population to db
    path(r'research/db/<str:model_key>/', views.DbManager.as_view())  # Delete individual from OM
]
