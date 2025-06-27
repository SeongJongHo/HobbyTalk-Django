from django.urls import path

from categories.views import CategoryViewV1

urlpatterns = [
    path('', CategoryViewV1.as_view(), name='category-list'),
    path('/<int:category_id>', CategoryViewV1.as_view(), name='category-detail'),
]