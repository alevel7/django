from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name='index'),
    path("books", views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path("register", views.register, name='register'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='myBorrowed'),
    path('mybooks/borrowed', views.AllBorrowedBooksListView.as_view(), name='borrowedAll'),
    #path('book/<int:pk>', views.book_detail_view, name='book-detail'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'), 
]

urlpatterns += [ 
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'), 
]
