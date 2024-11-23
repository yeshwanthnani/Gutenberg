from django.urls import path
from .views import BooksBookListView

urlpatterns = [
    path('', BooksBookListView.as_view(), name='books-list'),
]
