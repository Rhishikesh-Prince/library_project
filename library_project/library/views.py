from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Borrowing




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    return render(request, 'library/home.html')


def book_list(request):
    q = request.GET.get('q', '')
    qs = Book.objects.all()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q))
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    return render(request, 'library/book_list.html', {'books': books, 'q': q})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    
    if book.available_copies() <= 0:
        messages.error(request, "No copies available.")
        return redirect('book_detail', pk=pk)

   
    active_count = Borrowing.objects.filter(user=user, returned_at__isnull=True).count()
    if active_count >= getattr(settings, 'BORROW_LIMIT', 3):
        messages.error(request, f"Borrow limit reached ({settings.BORROW_LIMIT}).")
        return redirect('book_detail', pk=pk)

    
    if Borrowing.objects.filter(user=user, book=book, returned_at__isnull=True).exists():
        messages.error(request, "You already borrowed this book.")
        return redirect('book_detail', pk=pk)

    borrowed_at = timezone.now()
    due_at = borrowed_at + timedelta(days=getattr(settings, 'LOAN_DAYS', 14))
    Borrowing.objects.create(user=user, book=book, borrowed_at=borrowed_at, due_at=due_at)
    messages.success(request, f"Book borrowed. Due date: {due_at.date()}")
    return redirect('my_borrowings')

@login_required
def return_book(request, pk):
    borrowing = get_object_or_404(Borrowing, pk=pk, user=request.user)
    if borrowing.returned_at:
        messages.info(request, "Already returned.")
    else:
        borrowing.returned_at = timezone.now()
        borrowing.save()
        messages.success(request, "Book returned.")
    return redirect('my_borrowings')

@login_required
def my_borrowings(request):
    active = Borrowing.objects.filter(user=request.user, returned_at__isnull=True).order_by('-borrowed_at')
    history = Borrowing.objects.filter(user=request.user, returned_at__isnull=False).order_by('-returned_at')
    return render(request, 'library/my_borrowings.html', {'active': active, 'history': history})
