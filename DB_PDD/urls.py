# -*- coding: utf-8 -*-
"""DB_PDD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('Json/', include('JSON_DB.urls')),
    path('RulesAuto/', include('DB_RULES.urls')),
    path('Roads/', include('DB_ROADS.urls')),
    path('Quizes/', include('QUIZES.urls')),
    path('Classes', include('DB_CLASSES.urls')),
    path('Profiles/', include('PROFILES_DB.urls')),
    path('Links/', include('DB_LINKS.urls')),
]
