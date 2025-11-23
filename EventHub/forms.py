from django import forms
from .models import Event, Comment, EventAttachment, Category


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jeśli nie ma kategorii, ukryj pole kategorii
        if not Category.objects.exists():
            self.fields.pop('category', None)
        else:
            self.fields['category'].empty_label = "Wybierz kategorię"
            self.fields['category'].queryset = Category.objects.all()

    class Meta:
        model = Event
        fields = [
            'title', 'short_description', 'description', 'location',
            'start_date', 'end_date', 'category', 'max_participants', 'status'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Szczegółowy opis wydarzenia...'
            }),
            'short_description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Krótki opis wyświetlany na liście wydarzeń...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa wydarzenia...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Miejsce wydarzenia...'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Tytuł wydarzenia',
            'short_description': 'Krótki opis',
            'description': 'Pełny opis',
            'location': 'Miejsce',
            'start_date': 'Data rozpoczęcia',
            'end_date': 'Data zakończenia',
            'category': 'Kategoria',
            'max_participants': 'Maksymalna liczba uczestników',
            'status': 'Status',
        }
        help_texts = {
            'max_participants': 'Pozostaw 0 dla nieograniczonej liczby uczestników',
            'short_description': 'Maksymalnie 500 znaków',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Dodaj komentarz...'
            })
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = EventAttachment
        fields = ['file', 'name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa załącznika...'
            }),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }