from django.contrib import admin

from .models import Author, Genre, Book, BookInstance

# Register your models here.

admin.site.register(Genre)
# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)

# ------------------------------------------------
@admin.register(Author)    # or admin.site.register(Author, AuthorAdmin)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# ------------------------------------------------

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance    # declaring inlines, of type TabularInline (horizontal layout) or StackedInline 

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# ------------------------------------------------

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
   # grouping information
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

# ------------------------------------------------
