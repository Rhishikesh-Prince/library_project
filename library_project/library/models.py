from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def available_copies(self):
        active = self.borrowing_set.filter(returned_at__isnull=True).count()
        return max(self.total_copies - active, 0)

class Borrowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} — {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.due_at:
            self.due_at = self.borrowed_at + timedelta(days=getattr(settings, 'LOAN_DAYS', 14))
        super().save(*args, **kwargs)
