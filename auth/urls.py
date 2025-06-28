from django.urls import path

from auth.views import SignUpViewV1, SignInViewV1

urlpatterns = [
    path('/sign-up', SignUpViewV1.as_view(), name='sign-up'),
    path('/sign-in', SignInViewV1.as_view(), name='sign-in'),
]