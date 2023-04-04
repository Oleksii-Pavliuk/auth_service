from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserAuth.as_view()),
    path('health', views.health_check), #Consul
]
