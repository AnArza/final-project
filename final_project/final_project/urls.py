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
from django.urls import path, include

from .api.category import CategoryView
from .api.creative import CreativeView
from .api.config import ConfigView
from .api.campaign import CampaignView
from .api.bid import BidView
from .api.history import HistoryView
from .api.notify import NotifyView
from .api.login_register import log_reg, create_user, login_view, success_view, home

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("api/creatives/", CreativeView.as_view(), name="creatives"),
    path("api/creatives/<int:id>/", CreativeView.check_view, name="creatives_id"),
    path("api/categories/", CategoryView.as_view(), name="categories"),
    path("api/categories/<str:code>/", CategoryView.check_view, name="categories_id"),
    path("api/campaigns/<int:id>/", CampaignView.check_view, name="campaign_id"),
    path("api/campaigns/", CampaignView.as_view(), name="campaign"),
    path("rtb/bid/", BidView.as_view(), name="bid"),
    path("rtb/notify/", NotifyView.as_view()),
    path("game/configure/", ConfigView.as_view(), name="config"),
    path("game/configure/delete/", ConfigView.delete, name="config_delete"),
    path("history/", HistoryView.as_view()),
    path('', log_reg, name="log_reg"),
    path('create_user/', create_user, name='create_user'),
    path('login/', login_view, name='login'),
    path('success/', success_view, name="success"),
    path('home/', home, name="home")

    # path("rtb/bid/", BidView.as_view())
]
