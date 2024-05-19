from django.contrib import admin
from django.urls import path
from .views import userView, addReceiptView, deleteReceiptView, landingView, createUserView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('user/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('user/add/', addReceiptView, name='add'),
    path('user/delete/', deleteReceiptView, name='delete'),
    path('user/<int:userId>', userView, name='user'),
    path('login/createUser/', createUserView, name='createUser'),
    path('', landingView, name='landing'),
]
