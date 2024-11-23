from rest_framework import serializers
from .models import *


class BooksAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksAuthor
        fields = ['name', 'birth_year', 'death_year']


class BooksBookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksBookshelf
        fields = ['name']


class BooksLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksLanguage
        fields = ['code']


class BooksSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksSubject
        fields = ['name']


class BooksFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksFormat
        fields = ['mime_type', 'url']


class BooksBookSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    download_links = serializers.SerializerMethodField()

    class Meta:
        model = BooksBook
        fields = ['title', 'author_info', 'genre', 'language', 'subjects', 'bookshelves', 'download_links']

    def get_author_info(self, obj):
        authors = BooksAuthor.objects.filter(
            id__in=BooksBookAuthors.objects.filter(book_id=obj.id).values('author_id')
        )
        author_details = []
        for author in authors:
            birth_info = f"born {author.birth_year}" if author.birth_year else "unknown"
            death_info = f"died {author.death_year}" if author.death_year else "unknown"
            author_details.append(f"{author.name} ({birth_info} - {death_info})")
        return author_details

    def get_genre(self, obj):
        bookshelves = BooksBookshelf.objects.filter(
            id__in=BooksBookBookshelves.objects.filter(book_id=obj.id).values('bookshelf_id')
        )
        return [bookshelf.name for bookshelf in bookshelves]

    def get_language(self, obj):
        languages = BooksLanguage.objects.filter(
            id__in=BooksBookLanguages.objects.filter(book_id=obj.id).values('language_id')
        )
        return [language.code for language in languages]

    def get_subjects(self, obj):
        subjects = BooksSubject.objects.filter(
            id__in=BooksBookSubjects.objects.filter(book_id=obj.id).values('subject_id')
        )
        return [subject.name for subject in subjects]

    def get_bookshelves(self, obj):
        bookshelves = BooksBookshelf.objects.filter(
            id__in=BooksBookBookshelves.objects.filter(book_id=obj.id).values('bookshelf_id')
        )
        return [bookshelf.name for bookshelf in bookshelves]

    def get_download_links(self, obj):
        formats = BooksFormat.objects.filter(book_id=obj.id)
        return [{"mime_type": format.mime_type, "url": format.url} for format in formats]
