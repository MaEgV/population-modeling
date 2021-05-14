from django.urls import path
from. import views

urlpatterns = [
    path(r'research/<str:id>/', views.CreateResearch.as_view()),  # Load population from DB
    path(r'research/', views.CreateResearch.as_view()),  # Create new population
    path(r'research/<str:token>/run/', views.ResearchManage.as_view()),  # Run research with parameters(POST)
    path(r'research/<str:token>/add/', views.ResearchManage.as_view())  # Add individual to population(POST)
]