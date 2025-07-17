"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

from config.views import HealthView

urlpatterns = [
    path('api/query/v1/categories', include("categories.urls")),
    path('api/command/v1/auth', include("auth.urls")),
    path('api/command/v1/open-chat-rooms', include("open_chats.urls")),
    path('api/query/v1/open-chat-rooms', include("open_chats.query_urls")),
    path('health', HealthView.as_view(), name='health'),
]