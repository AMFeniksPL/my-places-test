from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name="home"),
    path('place/<str:pk>/', views.place, name='place'),
    path('place/<int:place_id>/topic/<int:topic_id>/', views.topic, name='topic'),
    path('create-place/', views.create_place, name='create-place'),
    path('place/<int:place_id>/create-topic/', views.create_topic, name='create-topic'),
    path('update-place/<str:pk>/', views.update_place, name='update-place'),
    path('update-topic/<str:pk>/', views.update_topic, name='update-topic'),
    path('delete-place/<str:pk>/', views.delete_place, name='delete-place'),
    path('delete-topic/<str:pk>/', views.delete_topic, name='delete-topic'),
    path('add-file/<str:pk>/', views.add_file, name='add-file'),
    path('find', views.find, name='find'),
    path('no-place', views.no_place, name='no-place'),
    path('place-password/<str:pk>/', views.place_password, name='place_password'),
]