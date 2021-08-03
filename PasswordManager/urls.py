"""PasswordManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('safe.urls')),
    path('login/',user_views.login_view,name="login"),
    path('logout/',user_views.logout_view,name="logout"),
    path('register/',user_views.register,name="register"),
    path('account-activate/<token>',user_views.account_activate,name="account-activate"),
    path('reset-password/',user_views.reset_password,name='reset-password'),
    path('reset-password-confirm/<token>',user_views.reset_password_confirm,name='reset-password-confirm'),
    path('profile/',user_views.profile,name='profile'),
    path('profile/master-key/',user_views.master_key,name="master-key")
]

if settings.DEBUG == True:
    urlpatterns +=  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
