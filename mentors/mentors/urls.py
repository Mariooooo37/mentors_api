from api.views import (
    RegistrationView,
    UserView,
    UserDetailView,
    LogoutView,
    CustomTokenObtainPairView,
)

from django.urls import path
from django.contrib import admin
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("users/", UserView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
