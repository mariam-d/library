
from telnetlib import STATUS
from django.http import Http404
from django.shortcuts import render , get_object_or_404

from .models import Book, Author, BookInstance, Genre
from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy

# from django.contrib.auth.decorators import login_required    # for function => @login_required
from django.contrib.auth.mixins import LoginRequiredMixin      # for class

# from django.contrib.auth.decorators import permission_required  # for function => @permission_required('catalog.can_mark_returned')
from django.contrib.auth.mixins import PermissionRequiredMixin  # permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')


# Create your views here.

# =================================================================
# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
def index(request):  # home page
   
   # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()  # Available books (status = 'a')
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

# =================================================================

class BookListView(ListView):
    model = Book  #book_list
    paginate_by = 3    #http://127.0.0.1:8000/catalog/books/?page=2

    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    def get_queryset(self):
          return Book.objects.filter(title__icontains='b')[:5] 

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

# =================================================================

class BookDetailView(DetailView):
    model = Book   #book or object

    # def book_detail_view(request, primary_key):
    #     try:
    #         book = Book.objects.get(pk=primary_key)
    #     except Book.DoesNotExist:
    #         raise Http404('Book does not exist')

    #     return render(request, 'catalog/book_detail.html', context={'book': book})

    def book_detail_view(request, primary_key):
            book = get_object_or_404(Book, pk=primary_key)
            return render(request, 'catalog/book_detail.html', context={'book': book})

# =================================================================

class AuthorListView(ListView):

    model = Author  #author_list
    paginate_by = 3   
   
    def get_queryset(self):
          return Author.objects.all() 
    
# =================================================================

class AuthorDetailView(DetailView):
    model = Author  

    def book_detail_view(request, primary_key):
            author = get_object_or_404(Book, pk=primary_key)
            return render(request, 'catalog/author_detail.html', context={'author': author})

# =================================================================

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# =================================================================    

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

# # =================================================================   

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn' ,'genre' ]
    initial = {'date_of_death': '11/06/2020'}

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

# # =================================================================       

import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm , RenewBookModelForm

# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
# def renew_book_librarian(request, pk):

#     book_instance = get_object_or_404(BookInstance, pk=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('my-borrowed') )

#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

#         # RenewBookModelForm(initial={'due_back': proposed_renewal_date}

#     context = {
#         'form': form,
#         'book_instance': book_instance,
#     }

#     return render(request, 'catalog/book_renew_librarian.html', context)

#+++++++++++++++++++++++++++++++

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):

    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

        # RenewBookModelForm(initial={'due_back': proposed_renewal_date}

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)