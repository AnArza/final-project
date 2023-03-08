"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from .api.category import CategoryView
from .api.creative import CreativeView
from .api.bid import BidView
from .api.config import ConfigView
from .api.bid import BidView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("creatives/", CreativeView.as_view()),
    path("creatives/<int:id>/", CreativeView.check_view),
    path("categories/", CategoryView.as_view()),
    path("categories/<str:code>/", CategoryView.check_view),
    path("rtb/bid/", BidView.as_view()),
    path("game/configure/", ConfigView.as_view()),
    path("game/configure/delete/", ConfigView.delete),
    path("rtb/bid/", BidView.as_view())
]
