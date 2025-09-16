from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('get-response/', views.get_bot_response, name='get_bot_response'),
]
