from django.urls import path
from .views import HomeView, BoilerDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('boiler/<int:pk>/', BoilerDetailView.as_view(), name='boiler_detail'),
]
