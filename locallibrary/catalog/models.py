from django.db import models
from django.urls import reverse
import uuid #required for unique book instances
#This model will be used to store information about the book category
class Genre(models.Model):
        """Model representing a book genre."""
        name = models.CharField(max_length = 200, help_text = 'Enter a book genre (e.g Science Fiction)')

        def __str__(self):
            """String for representing the Model object."""
            return self.name
        #no verbose name defined so the field will be called Name in forms.


#book model represents all information about an available book in a general sense, but not a particular physical "instance" or "copy" available for loan.
class Book(models.Model):
        """Model representing a book (but not a specific copy of a book)."""
        title = models.CharField(max_length = 200)
        author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)# Foreign Key used because book can only have one author.  Author as a string rather than object because it hasn't been declared yet in the file
        summary = models.TextField(max_length = 1000, help_text = 'Enter a brief description of the book ')
        isbn = models.CharField('ISBN', max_length = 13, help_text = '13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN number</a>')
        genre = models.ManyToManyField(Genre, help_text = 'select a genre for the book ')

        def genre_display(self):
            return ', '.join(genre.name for genre in self.genre.all()[:3])
        genre_display.short_description = 'Genre '
        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('book-detail', args = [str(self.id)])


#represents a specific copy of a book that someone might borrow, and includes information about whether the copy is available or on what date it is expected back, "imprint" or version details, and a unique id for the book in the library.
class BookInstance(models.Model):
        """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
        id = models.UUIDField(primary_key = True, default = uuid.uuid4,help_text = 'Unique ID for this particular book acrossthe whole library ')
        book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True)
        imprint = models.CharField(max_length = 200)
        due_back = models.DateField(null = True, blank = True)

        LOAN_STATUS = (
            ('m', 'Maintainance'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

        status = models.CharField(
            max_length = 1,
            choices = LOAN_STATUS,
            blank = True,
            default = 'm',
            help_text = 'Book availability',
        )


        class Meta:
            ordering = ['due_back']

        def __str__(self):
            return f'{self.id} ({self.book.title})'


class Author(models.Model):
        """Model representing an author."""
        first_name = models.CharField(max_length = 100)
        last_name = models.CharField(max_length = 100)
        date_of_birth = models.DateField(null = True, blank = True)
        date_of_death = models.DateField('Died', null = True, blank = True)

        class Meta:
            ordering = ['last_name', 'first_name']

        def get_absolute_url(self):
            return reverse('author-detail', args = [str(self.id)])

        def __str__(self):
            return f'{self.last_name}, {self.first_name}'

