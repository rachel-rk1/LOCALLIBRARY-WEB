from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""
    #generate counts of some of the main objects
    num_books = Book.objects.all().count()#objects.all will fetch the  records
    num_instances = BookInstance.objects.all().count()


    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    #The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_author': num_authors,
    }
    #rendeer the HTML template index.html with data in context variable
    return render(request, 'index.html', context = context)