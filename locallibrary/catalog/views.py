import datetime
from django.shortcuts import render
from catalog.forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
"""using generic views starts here"""

class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    initial ={"date_of_death":"05/01/2018"}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

"""using generic views end here"""


class AllBorrowedBooksListView(LoginRequiredMixin, generic.ListView):
    '''generice class-based view to list all borrowed books to librarian'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_for_librarian.html'
    def get_queryset(self):
        return BookInstance.objects.all().filter(status__exact='o')
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user.""" 
    model = BookInstance  
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10 
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')

        
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2
    context_object_name = 'book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='apart')[:5] # Get 5 books containing the title war
    queryset = Book.objects.all()
    template_name = 'catalog/book_list.html'  # Specify your own template name/location

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'catalog/author_list.html'


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

# def book_detail_view(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'catalog/book_detail.html', context={'book': book})
def register(request):
    return render(request, 'catalog/register.html')

@login_required
def index(request):
    """view function for home page of site"""

    #generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available books (status ='a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

     # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()

    #number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits':num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """view function for renewing a new book instance by librarian"""
    book_instance = get_object_or_404(BookInstance,pk=pk)
    #if this is a post request then process the form
    if request.method == 'POST':
        #create a form instance and populate it with data from the request (Binding)
        form = RenewBookForm(request.POST)


        #check if form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowedAll') )
        
    #if this is a get or any other method,create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        context = {
            'form': form,
            'book_instance': book_instance,
            }
    return render(request, 'catalog/book_renew_librarian.html', context)
