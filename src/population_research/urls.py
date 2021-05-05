from django.urls import path
from. import views

urlpatterns = [
    path(r'research/<int:i>/', views.Research.as_view()),
    path(r'research/', views.Research.as_view())
]