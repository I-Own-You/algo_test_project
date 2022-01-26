from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


urlpatterns = format_suffix_patterns([
    path('', views.products, name='products'),

    path('<int:id>/', views.single_product, name='single_product'),
    path('add-product/', views.add_product, name='add-product'),
    path('edit-product/<int:id>', views.edit_product, name='edit-product'),
    path('remove-product/<int:id>', views.remove_product, name='remove-product'),

    path('products-list/', views.products_list, name='car-list'),
    path('products-list/<int:pk>/', views.product_detail, name='car-detail'),
    path('api-root/', views.api_root),


    path('car-images/<int:pk>/', views.images_detail, name='images-detail'),

    path('openapi/', get_schema_view(), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
])
