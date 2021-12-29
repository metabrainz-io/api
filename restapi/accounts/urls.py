from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import (
    MyObtainTokenPairView,
    LoginViewSet,
    LogoutViewSet,
    SomeActionView
)


urlpatterns = [
    path('login/<str:c_addr>', LoginViewSet.as_view({
        'get': 'login_request',
    })),
    path('login/', LoginViewSet.as_view({
        'get': 'login_request',
        'post': 'login_authenticate'
    })),
    path('logout/', LogoutViewSet.as_view()),
    # NOTE: Some endpoints for tesing purposes
    path('someaction/', SomeActionView.as_view({
        'get': 'get_account'
    })),
    # NOTE: Do not use this!!! Tokens can be retrieved simply using a c_addr and password
    path('token/', MyObtainTokenPairView.as_view(), name='get_user_token'),
    # NOTE: Use this to validate refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
