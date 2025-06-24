from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('newview/', views.newview, name='view'),
    path('add-book/', views.add_book, name='add-book'),  
    path('get-books/', views.get_books, name='get-books'),
    path('all_books/', views.get_all_books, name='all_books'),
    path('getall/', views.getall_books, name='getall')
]