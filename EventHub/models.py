import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from SWBO_Project import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Wersja robocza'),
        ('published', 'Opublikowane'),
        ('cancelled', 'Anulowane'),
    ]

    title = models.CharField(max_length=200, verbose_name="Tytuł")
    description = models.TextField(verbose_name="Opis")
    short_description = models.TextField(max_length=500, verbose_name="Krótki opis")
    location = models.CharField(max_length=200, verbose_name="Miejsce")
    start_date = models.DateTimeField(verbose_name="Data rozpoczęcia")
    end_date = models.DateTimeField(verbose_name="Data zakończenia")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    participants = models.ManyToManyField(User, through='Participation', related_name='events_participating')
    max_participants = models.PositiveIntegerField(default=0, verbose_name="Maksymalna liczba uczestników")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def is_upcoming(self):
        return self.start_date > timezone.now()

    def available_spots(self):
        if self.max_participants == 0:
            return "Bez limitu"
        registered = self.participants.count()
        return self.max_participants - registered


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'event']


class EventAttachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='event_attachments/%Y/%m/%d/')
    name = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=EventAttachment)
def delete_attachment_file(sender, instance, **kwargs):
    """
    Usuwa plik z systemu plików gdy obiekt EventAttachment jest usuwany.
    """
    if instance.file:
        try:
            file_path = instance.file.path
            if os.path.isfile(file_path):
                os.remove(file_path)
                # Spróbuj usunąć puste katalogi
                delete_empty_directories(file_path)
        except Exception as e:
            # Logowanie błędu, ale nie przerywamy działania
            print(f"Błąd podczas usuwania pliku: {e}")


def delete_empty_directories(file_path):
    """
    Rekurencyjnie usuwa puste katalogi zaczynając od katalogu pliku.
    """
    directory = os.path.dirname(file_path)

    while directory and directory != settings.MEDIA_ROOT:
        try:
            if not os.listdir(directory):
                os.rmdir(directory)
                directory = os.path.dirname(directory)
            else:
                break
        except OSError:
            break


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']