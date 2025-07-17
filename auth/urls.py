from django.urls import path

from auth.views import AuthViewV1, SignInViewV1

urlpatterns = [
    path('/sign-up', AuthViewV1.as_view(), name='sign-up'),
    path('/refresh-token', SignInViewV1.as_view(), name='refresh-token'),
    path('/sign-in', SignInViewV1.as_view(), name='sign-in'),
    path('/logout', AuthViewV1.as_view(), name='logout'),
]