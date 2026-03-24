from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from myproject.store.apps import StoreConfig
from myproject.store.views import product_list

app_name = StoreConfig.name

urlpatterns = [path("", product_list)]
