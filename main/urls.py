from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('solutions', views.solutions, name='solutions'),
    path('delete/<int:id>/', views.delete)
]
