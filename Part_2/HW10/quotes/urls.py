from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='index'),
    path('quote/', views.add_quote, name='add_quote'),
    path('tag/', views.tag, name='tag'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('author/add/', views.add_author, name='add_author'),
]