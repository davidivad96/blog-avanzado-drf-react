from django.urls import path

from .views import *


urlpatterns = [
    path('categories', CategoriesView.as_view()),
]
