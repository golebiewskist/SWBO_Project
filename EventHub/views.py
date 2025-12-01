from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q, Count
from .models import Event, Category, Participation, EventAttachment
from .forms import EventForm, CommentForm, AttachmentForm


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.filter(status='published')

        # Filtrowanie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )

        # ANNOTATE: Obliczanie liczby uczestników dla KAŻDEGO zapytania
        # Używamy distinct=True dla bezpieczeństwa na wypadek zduplikowanych wierszy
        queryset = queryset.annotate(participants_count=Count('participants', distinct=True))

        # Sortowanie
        sort = self.request.GET.get('sort', '-start_date')

        # Lista bezpiecznych pól do sortowania (w tym nowe participants_count)
        valid_sort_fields = ['title', 'start_date', 'end_date', 'created_at', 'participants_count']

        if sort.lstrip('-') in valid_sort_fields:  # lstrip('-') usuwa minus
            queryset = queryset.order_by(sort)
        else:
            # Domyślne sortowanie, jeśli podano nieprawidłowe pole
            queryset = queryset.order_by('-start_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['is_participating'] = False
        if self.request.user.is_authenticated:
            context['is_participating'] = Participation.objects.filter(
                user=self.request.user, event=self.object
            ).exists()
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_exist'] = Category.objects.exists()
        return context

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Wydarzenie zostało utworzone!')
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_exist'] = Category.objects.exists()
        return context

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

    def form_valid(self, form):
        messages.success(self.request, 'Wydarzenie zostało zaktualizowane!')
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Wydarzenie zostało usunięte!')
        return super().delete(request, *args, **kwargs)


@login_required
def participate_toggle(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        participation, created = Participation.objects.get_or_create(
            user=request.user,
            event=event
        )

        if created:
            messages.success(request, 'Zapisano na wydarzenie!')
        else:
            participation.delete()
            messages.success(request, 'Wypisano z wydarzenia!')

    return redirect('event-detail', pk=pk)


@login_required
def add_comment(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            messages.success(request, 'Komentarz dodany!')

    return redirect('event-detail', pk=pk)


@login_required
def my_events(request):
    organized = Event.objects.filter(organizer=request.user)
    participating = Event.objects.filter(participants=request.user)

    return render(request, 'events/my_events.html', {
        'organized_events': organized,
        'participating_events': participating
    })


@login_required
def add_attachment(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Tylko organizator może dodawać załączniki
    if request.user != event.organizer:
        messages.error(request, 'Nie masz uprawnień do dodawania załączników.')
        return redirect('event-detail', pk=pk)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.event = event
            attachment.save()
            messages.success(request, 'Załącznik został dodany!')
        else:
            messages.error(request, 'Błąd podczas dodawania załącznika.')

    return redirect('event-detail', pk=pk)


@login_required
def delete_attachment(request, pk):
    attachment = get_object_or_404(EventAttachment, pk=pk)
    event_pk = attachment.event.pk

    # Tylko organizator może usuwać załączniki
    if request.user == attachment.event.organizer:
        attachment.delete()
        messages.success(request, 'Załącznik został usunięty!')
    else:
        messages.error(request, 'Nie masz uprawnień do usuwania załączników.')

    return redirect('event-detail', pk=event_pk)