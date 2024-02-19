"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Import necessary modules/classes
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views         # Import views module from the current directory (assuming this urls.py is in the same directory as views.py)
  

# Define urlpatterns, a list of URL patterns for the Django application
urlpatterns = [
    # Define URL pattern for the home page
    path('', views.home, name='home'),
    # Define URL pattern for the sign-in page
    path('signin', views.signin, name="signin"),
    # Define URL pattern for the sign-up page
    path('signup', views.signup, name="signup"),
    # Define URL pattern for the sign-out page
    path('signout', views.signout, name="signout"),
    # Define URL pattern for the activation page with two dynamic segments (uidb64 and token)
    path('activate/<uidb64>/<token>', views.activate, name="activate"),

    # for reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
] 

# This is the list of URL patterns that Django's URL resolver will use to route requests to the appropriate view functions.
# Each URL pattern consists of three main parts: the URL pattern itself, the corresponding view function, and a name identifier for easy reference in templates and views.

 