from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('post/<int:pk>/', views.post_list, name='post_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<int:pk>/', views.post_details, name='post_details'),
    path('<int:pk>/edit', views.post_edit, name='post_edit'),
    path('create/', views.post_create, name='post_create'),
    path('drafts/', views.post_drafts, name='post_drafts'),
    path('<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('<int:pk>/remove/', views.post_remove, name='post_remove'),

]
