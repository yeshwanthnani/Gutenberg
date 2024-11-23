from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import *
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from .filters import *
from .pagination import *
from .serializers import BooksBookSerializer

class BooksBookListView(ListAPIView):
    queryset = BooksBook.objects.all()
    serializer_class = BooksBookSerializer
    pagination_class = CustomPagination

    filter_backends = (OrderingFilter, SearchFilter, filters.DjangoFilterBackend)
    filterset_class = BooksBookFilter
    search_fields = ['title', 'gutenberg_id', 'media_type']
    ordering_fields = ['id', 'title', 'download_count']
    ordering = ['id']

    def get_queryset(self):
        request = self.request
        author_name_filter = request.query_params.get('author_name', None)
        bookshelf_id_filter = request.query_params.get('bookshelf_id', None)
        language_code_filter = request.query_params.get('language_code', None)
        subject_name_filter = request.query_params.get('subject_name', None)
        mime_type_filter = request.query_params.get('mime_type', None)
        

        queryset = BooksBook.objects.all()

        #Applying filtering
        if author_name_filter:
            queryset = queryset.filter(
                booksbookauthors__author__name__icontains=author_name_filter
            )

        if bookshelf_id_filter:
            queryset = queryset.filter(
                booksbookbookshelves__bookshelf__id=bookshelf_id_filter
            )

        if language_code_filter:
            queryset = queryset.filter(
                booksbooklanguages__language__code=language_code_filter
            )

        if subject_name_filter:
            queryset = queryset.filter(
                booksbooksubjects__subject__name__icontains=subject_name_filter
            )

        if mime_type_filter:
            queryset = queryset.filter(
                booksformat__mime_type=mime_type_filter
            )

        return queryset
