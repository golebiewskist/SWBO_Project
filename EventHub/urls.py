from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('event/new/', views.EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
    path('event/<int:pk>/participate/', views.participate_toggle, name='event-participate'),
    path('event/<int:pk>/attachment/', views.add_attachment, name='add-attachment'),
    path('attachment/<int:pk>/delete/', views.delete_attachment, name='delete-attachment'),
    path('event/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('my-events/', views.my_events, name='my-events'),
]