from django.urls import path
from .views import register_agent, list_agents, search_agents

urlpatterns = [
    path('register', register_agent),
    path('list', list_agents),
    path('search', search_agents),
]