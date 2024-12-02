from phonenumber_field.formfields import PhoneNumberField
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from users.models import User


class UserBaseSerializer(ModelSerializer):
    """
    Базовый сериализатор пользователя.
    """

    phone = CharField(validators=PhoneNumberField().validators)

    class Meta:
        model = User
        fields = ["phone"]


class UserLoginSerializer(ModelSerializer):
    """
    Сериализатор для аутентификации пользователя.
    """

    phone = CharField(validators=PhoneNumberField().validators)

    class Meta:
        model = User
        fields = ["phone", "verification_code"]


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор просмотра профиля пользователя.
    """

    class Meta:
        model = User
        fields = ["phone", "invite_code", "first_name", "last_name", "invited_by"]


class UserWithReferralsSerializer(ModelSerializer):
    """
    Сериализатор просмотра профиля пользователя с рефералами.
    """

    referrals = SerializerMethodField()

    def get_referrals(self, user):
        return [str(user.phone) for user in User.objects.filter(invited_by=user)]

    class Meta:
        model = User
        fields = [
            "phone",
            "invite_code",
            "first_name",
            "last_name",
            "invited_by",
            "referrals",
        ]


class InviteCodeSerializer(Serializer):
    """
    Сериализатор инвайт-кода.
    """

    code = CharField(max_length=6)
