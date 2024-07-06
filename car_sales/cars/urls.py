from django.urls import path
from .views import HomeView, CarDetailView, ProfileView, buy_car, register, add_comment, order_history,SearchView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('buy/<int:pk>/',buy_car , name='buy_car'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
    path('comment/<int:pk>/', add_comment, name='add-comment'),
    path('orders/', order_history, name='order-history'),
    path('search/', SearchView.as_view(), name='search'),
]
