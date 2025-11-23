from django.contrib import admin
from .models import Event, Category, Participation, EventAttachment, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'event_count']
    list_editable = ['color']
    search_fields = ['name']
    list_per_page = 20

    def event_count(self, obj):
        return obj.event_set.count()

    event_count.short_description = 'Liczba wydarzeń'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'start_date', 'location', 'category', 'status', 'participants_count',
                    'created_at']
    list_filter = ['category', 'status', 'start_date', 'created_at']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    list_per_page = 25
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('title', 'short_description', 'description', 'organizer')
        }),
        ('Szczegóły wydarzenia', {
            'fields': ('location', 'start_date', 'end_date', 'category')
        }),
        ('Ograniczenia i status', {
            'fields': ('max_participants', 'status')
        }),
        ('Metadane', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def participants_count(self, obj):
        return obj.participants.count()

    participants_count.short_description = 'Uczestnicy'


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at']
    list_filter = ['registered_at', 'event']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['registered_at']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'event')


@admin.register(EventAttachment)
class EventAttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'uploaded_at', 'file']
    list_filter = ['uploaded_at']
    search_fields = ['name', 'event__title']
    readonly_fields = ['uploaded_at']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'event', 'created_at', 'content_preview']
    list_filter = ['created_at', 'event']
    search_fields = ['author__username', 'event__title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Komentarz'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'event')

