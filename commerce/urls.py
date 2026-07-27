"""
URL configuration for commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from api.views import login, logout, register, item, shopping, sale, shopping_basket, checkout, view_orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login),
    path('api/logout/', logout),
    path('api/register/', register),
    # Items expects an item id to be passed in the URL to get specific item details.
    path('api/items/<int:item_id>/', item),
    path('api/shopping/', shopping),
    path('api/sale/', sale),
    path('api/shopping_basket/', shopping_basket),
    path('api/checkout/', checkout),
    path('api/view_orders/', view_orders)
]
