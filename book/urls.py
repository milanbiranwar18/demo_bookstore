from django.urls import path
from . import views

urlpatterns = [
    path('book_app/', views.Books.as_view(), name='book_app'),
    path('book_app/<int:pk>/', views.Books.as_view(), name='book_app'),
]