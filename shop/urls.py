from django.urls import path
from . import views
# from .views import ask_ai

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart_view, name='cart'),
path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('ai-recommendation/', views.ai_recommendation, name='ai_recommendation'),
]
