from django.urls import path
from. import views

urlpatterns = [
    path(r'research/<int:population_id>/', views.CreateResearch.as_view()),  # Load population from DB
    path(r'research/', views.CreateResearch.as_view()),  # Create new population
    path(r'research/<str:token>/run/', views.ResearchRun.as_view()),  # Run research with parameters(POST)
    path(r'research/<str:token>/add/', views.ResearchAddIndividual.as_view()),  # Add individual to population(POST)
    path(r'research/<str:token>/delete/', views.ResearchManage.as_view()),  # Delete individual from OM
    path(r'research/<str:token>/save/', views.ResearchManage.as_view())  # Save population to db
]
