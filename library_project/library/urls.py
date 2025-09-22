from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.book_list, name='books_list'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('books/', views.book_list, name='books_list'),
    path('<int:pk>/', views.book_detail, name='book_detail'),
    path('<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrowings/<int:pk>/return/', views.return_book, name='return_book'),
    path('my/', views.my_borrowings, name='my_borrowings'),
]