from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm, UserPermissionsForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Konto zostało utworzone!')
            return redirect('event-list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Twój profil został zaktualizowany!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def custom_logout(request):
    logout(request)
    messages.success(request, 'Zostałeś wylogowany!')
    return redirect('event-list')


def can_create_events(user):
    return user.is_authenticated and (
            user.is_superuser or
            hasattr(user, 'userprofile') and user.userprofile.can_create_events
    )


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


# Widok zarządzania użytkownikami - TYLKO DLA SUPERUSERA
@superuser_required
def user_management(request):
    users = User.objects.all().select_related('userprofile').order_by('-date_joined')
    return render(request, 'users/user_management.html', {'users': users})


@superuser_required
def toggle_event_permission(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile
    profile.can_create_events = not profile.can_create_events
    profile.save()

    action = "przyznano" if profile.can_create_events else "cofnięto"
    messages.success(request, f'Uprawnienia do tworzenia wydarzeń {action} dla {user.username}')
    return redirect('user-management')


@superuser_required
def edit_user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile

    if request.method == 'POST':
        form = UserPermissionsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Uprawnienia użytkownika {user.username} zostały zaktualizowane!')
            return redirect('user-management')
    else:
        form = UserPermissionsForm(instance=profile)

    return render(request, 'users/edit_permissions.html', {
        'form': form,
        'user': user
    })