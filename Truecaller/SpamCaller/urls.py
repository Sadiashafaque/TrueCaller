"""
URL configuration for SpamCaller project.

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
from django.contrib import admin
from django.urls import path
from SpamCaller.views.RegisterView import RegisterProfileView, LoginView
from SpamCaller.views.ContactView import CreateContactAndMappingView
from SpamCaller.views.SpamView import MarkSpam
from SpamCaller.views.SearchView import SearchByName,SearchByNumber
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('spam/', MarkSpam.as_view()),
    path('searchname/', SearchByName.as_view()),
    path('searchnumber/', SearchByNumber.as_view()),
    path('contacts/', CreateContactAndMappingView.as_view()),
    path('signup/', RegisterProfileView.as_view()),
    path('login/', LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('admin/', admin.site.urls),
]
