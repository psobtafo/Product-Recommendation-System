from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/<int:user_id>/', views.get_recommendations, name='recommendations'),  # GET endpoint
    path('api/recommend', views.recommend, name='api_recommend'),  # POST endpoint for Supabase
    path('', views.home, name='home'),  # Home page
]





