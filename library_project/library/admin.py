from django.contrib import admin
from .models import Book, Borrowing

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'total_copies', 'available_copies_admin')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('author',)

    def available_copies_admin(self, obj):
        return obj.available_copies()
    available_copies_admin.short_description = 'Available copies'

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_at', 'due_at', 'returned_at', 'is_overdue')
    list_filter = ('returned_at',)
    search_fields = ('book__title', 'user__username')
    readonly_fields = ('borrowed_at',)

    
    def is_overdue(self, obj):
        return obj.returned_at is None and obj.due_at < timezone.now()
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
