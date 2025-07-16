from django.urls import path

from categories.views import CategoryViewV1, TrendingCategoryViewV1

urlpatterns = [
    path('/trending', TrendingCategoryViewV1.as_view(), name='trending-categories'),
    path('', CategoryViewV1.as_view(), name='category-list'),
    path('/<int:category_id>', CategoryViewV1.as_view(), name='category-detail'),
]