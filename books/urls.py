"""e_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

app_name = 'books'

urlpatterns = [
    path('', views.digital_books, name = 'digital_books'),
    
    path('view-book/', views.view_book, name = 'view_book'),
    path('add-book/', views.add_Book, name = 'add_book'),
    path('book-detail/<slug:slug>/', views.book_detail, name = 'book_detail'),
    path('delete-book/<str:pk>/', views.delete_book, name = 'delete_book'),
    
    path('search/', views.search, name = 'search'),
    # path( ' ', include('books.urls', namespace='books')),
]
