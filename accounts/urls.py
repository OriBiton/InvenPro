from django.urls import path
from .views import register_view,home_view,approve_user_view,reject_user_view,CustomLoginView,dashboard_view
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('register/', register_view, name='register'),
    path('', home_view, name='home'),  # זה יאפשר {% url 'home' %}
    path('approve/<int:user_id>/', approve_user_view, name='approve_user'),
    path('reject/<int:user_id>/', reject_user_view, name='reject_user'),
    path('login/', CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),


]
