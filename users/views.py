from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import (
    UserBaseSerializer,
    UserLoginSerializer,
    UserWithReferralsSerializer,
    InviteCodeSerializer,
)
from users.services import send_sms, generate_invite_code


class SMSCodeView(APIView):
    """
    Контроллер получения СМС-кода для входа или регистрации пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = self.serializer_class(data=request.data, context={"request": request})
        if ser.is_valid():
            phone = request.data.get("phone")
            code = send_sms(phone)
            user = User.objects.filter(phone=phone).first()
            if user:
                user.verification_code = code
            else:
                invite_code = generate_invite_code()
                user = User.objects.create(
                    phone=phone, verification_code=code, invite_code=invite_code
                )
            user.save()

            return Response({"detail": "Код отправлен."}, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Неверный формат номера телефона"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class UserLoginView(APIView):
    """
    Контроллер аутентификации пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        ser = self.serializer_class(data=request.data, context={"request": request})
        if ser.is_valid():
            phone = request.data.get("phone")
            code = request.data.get("verification_code")
            user = User.objects.filter(phone=phone, verification_code=code).first()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                user.verification_code = None
                user.save()
                return Response({"Token": token.key}, status=status.HTTP_200_OK)
            return Response(
                {"detail": "Неверный номер телефона или код подтверждения"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {"detail": "Неверный формат номера телефона или кода подтверждения"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер детального просмотра пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserWithReferralsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserWithReferralsSerializer(user)
        return Response(serializer.data)


class UserInviteCodeAPIView(UpdateAPIView):
    """
    Контроллер добавления инвайт-кода пользователя.
    """

    queryset = User.objects.all()
    serializer_class = InviteCodeSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user = request.user
        user_invited_by = user.invited_by
        if user_invited_by:
            return Response(
                {"detail": "Инвайт-код был введен ранее. Повторный ввод запрещен."},
                status=status.HTTP_409_CONFLICT,
            )
        invite_code = request.data.get("code")
        invited_by = User.objects.filter(invite_code=invite_code).first()
        if invited_by:
            user.invited_by = invited_by
            user.save()
            serializer = UserWithReferralsSerializer(user)
            return Response(serializer.data)
        return Response(
            {"detail": "Введен несуществующий инвайт-код."},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
