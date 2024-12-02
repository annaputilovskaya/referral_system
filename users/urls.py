from django.urls import path

from users.apps import UsersConfig
from users.views import (
    SMSCodeView,
    UserLoginView,
    UserRetrieveAPIView,
    UserInviteCodeAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("", SMSCodeView.as_view(), name="code"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserRetrieveAPIView.as_view(), name="profile"),
    path("invited/", UserInviteCodeAPIView.as_view(), name="invited"),
]
