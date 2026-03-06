from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('history/', views.history, name='history'),
    path('history/delete/<str:item_id>/', views.delete_history_item, name='delete_history_item'),
    path('clear-history/', views.clear_history, name='clear_history'),
]