from .models import CustomUser

from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации нового пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ["username", "password", "phone", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения и обновления информации о пользователе.
    """

    mentees = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="username"
    )
    mentor = serializers.SlugRelatedField(read_only=True, slug_field="username")
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone", "mentor", "mentees", "password"]

    def update(self, instance, validated_data):
        """
        Обновляет данные пользователя. Если указан новый пароль, он хэшируется перед сохранением.
        """
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class AssignMentorSerializer(serializers.Serializer):
    """
    Сериализатор для назначения наставника.
    """

    user_id = serializers.IntegerField(
        help_text="ID пользователя, которого нужно назначить наставником."
    )
