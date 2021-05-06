from django.urls import path
from. import views

urlpatterns = [
    path(r'research/', views.CreateResearch.as_view()),
    path(r'research/<str:token>/<str:action>', views.ManageResearch.as_view())
]