from django.urls import path

from auth.views import AuthViewV1

urlpatterns = [
    path('/sign-up', AuthViewV1.as_view(), name='sign-up'),
]