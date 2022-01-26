from django.urls.conf import path
from . import views


urlpatterns = [
    path('', views.user_list_api, name='user-list'),
    path('<int:pk>/', views.user_detail_api, name='user-detail'),
]
