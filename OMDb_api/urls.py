from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name="index"),
    path('title/<str:id>', views.Title, name="title")
]