
# Inherited classes from Djoser
from djoser.views import (
    UserViewSet, TokenCreateView, TokenDestroyView
)

from rest_framework.decorators import action

class MySiteAuthViews(UserViewSet):
    serializer_class = UserViewSet.serializer_class
    queryset = UserViewSet.queryset
    permission_classes = UserViewSet.permission_classes
    token_generator = UserViewSet.token_generator
    lookup_field = UserViewSet.lookup_field

    def permission_denied(self, request, **kwargs):
        return super().permission_denied(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset()
    
    def get_permissions(self):
        return super().get_permissions()
    
    def get_serializer_class(self):
        return super().get_serializer_class()
    
    def get_instance(self):
        return super().get_instance()
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @action(["get", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    def activation(self, request, *args, **kwargs):
        return super().activation(request, *args, **kwargs)
    def resend_activation(self, request, *args, **kwargs):
        return super().resend_activation(request, *args, **kwargs)
    def set_password(self, request, *args, **kwargs):
        return super().set_password(request, *args, **kwargs)
    def reset_password(self, request, *args, **kwargs):
        return super().reset_password(request, *args, **kwargs)
    def reset_password_confirm(self, request, *args, **kwargs):
        return super().reset_password_confirm(request, *args, **kwargs)
    def set_username(self, request, *args, **kwargs):
        return super().set_username(request, *args, **kwargs)
    def reset_username(self, request, *args, **kwargs):
        return super().reset_username(request, *args, **kwargs)
    def reset_username_confirm(self, request, *args, **kwargs):
        return super().reset_username_confirm(request, *args, **kwargs)


class MyTokenCreateView(TokenCreateView):

    serializer_class = TokenCreateView.serializer_class
    permission_classes = TokenCreateView.permission_classes

    def _action(self, serializer):
        return super()._action(serializer)

class MyTokenDestroyView(TokenDestroyView):

    permission_classes = TokenDestroyView.permission_classes

    def post(self, request):
        return super().post(request)