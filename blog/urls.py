from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('account/', include('django.contrib.auth.urls')),
    path('<int:pk>/', views.post_details, name='post_details'),
    path('<int:pk>/edit', views.post_edit, name='post_edit'),
    path('create/', views.post_create, name='post_create'),
]

