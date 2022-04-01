from product.views import productview
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('products/', productview, name='products'),
]
