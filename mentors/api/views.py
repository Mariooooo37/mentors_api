from .models import CustomUser
from .serializers import RegistrationSerializer, UserSerializer, AssignMentorSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Авторизация пользователя с получением пары токенов: access и refresh.
    """

    @extend_schema(
        description=(
                "Принимает учетные данные пользователя и возвращает пару JSON Web Token "
                "(access и refresh) для подтверждения подлинности."
        ),
        summary="Авторизация пользователя.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegistrationView(APIView):
    """
    Регистрация нового пользователя.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: RegistrationSerializer},
        summary="Регистрация пользователя.",
        description="Регистрация нового пользователя с указанием необходимых данных.",
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    """
    Получение списка всех пользователей.
    Назначение наставника для пользователя.
    Доступно только для аутентифицированных пользователей.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer(many=True)},
        summary="Список пользователей.",
        description="Возвращает список всех зарегистрированных пользователей.",
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Назначение наставника.",
        description=(
            "Позволяет текущему пользователю назначить другого пользователя своим наставником. "
            "Если у пользователя уже есть наставник, он заменяется на нового."
        ),
        request=AssignMentorSerializer,
    )
    def post(self, request):
        """
        Назначение наставника.
        """
        serializer = AssignMentorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        mentor = get_object_or_404(CustomUser, pk=user_id)

        if request.user == mentor:
            return Response(
                {"detail": "Вы не можете назначить себя своим наставником."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.mentor = mentor
        request.user.save()
        return Response(
            {"detail": f"{mentor.username} успешно назначен вашим наставником."},
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    """
    Получение и обновление данных пользователя.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        summary="Получение данных пользователя.",
        description="Возвращает информацию о пользователе.",
    )
    def get(self, request, pk):
        """
        Возвращает данные пользователя. Если запрашивается текущий пользователь,
        добавляется поле пароля.
        """
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.serializer_class(user)
        data = serializer.data

        if request.user == user:
            data["password"] = user.password

        return Response(data)

    @extend_schema(
        summary="Обновление данных пользователя.",
        description="Позволяет обновлять данные только текущего пользователя.",
    )
    def patch(self, request, pk):
        """
        Обновление данных пользователя.
        """
        user = get_object_or_404(CustomUser, pk=pk)
        if request.user != user:
            return Response(
                {"detail": "Вы можете изменять только свои данные."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    """
    Завершение сеанса пользователя.
    Удаляет все токены, связанные с текущим пользователем.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={205: None},
        summary="Выход.",
        description="Удаляет активные токены текущего пользователя, делая их недействительными.",
    )
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
