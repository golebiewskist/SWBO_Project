from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['can_create_events', 'bio', 'phone']


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'can_create_events')
    list_filter = ('is_staff', 'is_superuser', 'userprofile__can_create_events')

    def can_create_events(self, obj):
        return obj.userprofile.can_create_events

    can_create_events.boolean = True
    can_create_events.short_description = 'Może tworzyć wydarzenia'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)