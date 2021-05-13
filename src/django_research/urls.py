from django.urls import path
from. import views

urlpatterns = [
    path(r'research/', views.CreateResearch.as_view()),
    path(r'research/<str:id>/', views.CreateResearch.as_view()),
    path(r'research/<str:token>/build/', views.ResearchManage.as_view()),
    path(r'research/<str:token>/add/', views.ResearchManage.as_view())
]