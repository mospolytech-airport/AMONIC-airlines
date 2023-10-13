from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from authentication.models import User
from authentication.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data['email'])
        data = self.serializer_class(user).data

        refresh = RefreshToken.for_user(user)

        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token), 'data': data}

        return response

    @action(methods=['POST'], detail=False, url_path='login')
    def login(self, request):
        if 'email' not in request.data:
            raise ValidationError({'error': 'email must not be empty'})
        if 'password' not in request.data:
            raise ValidationError({'error': 'password must not be empty'})

        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound({'error': 'user with this email was not found'})

        if not user.check_password(request.data['password']):
            raise AuthenticationFailed({'error': 'password is not correct'})

        if not user.is_active:
            raise AuthenticationFailed({'error': 'user is not active'})
        
        # Получите текущее время входа
        current_login_time = timezone.now()
        
        # Получите существующие данные времени входа и выхода из JSON-поля
        login_logout_times = user.login_logout_times or {}
        
        # Добавьте время входа в JSON-поле
        login_logout_times[current_login_time.isoformat()] = None
        
        # Обновите JSON-поле
        user.login_logout_times = login_logout_times
        user.save()

        data = self.serializer_class(user).data

        refresh = RefreshToken.for_user(user)

        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token), 'data': data}

        return response

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_path='me')
    def get_user(self, request):
        user = request.user
        data = self.serializer_class(user).data

        return Response(data)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):

        # Получите текущее время выхода
        current_logout_time = timezone.now()
        
        # Получите существующие данные времени входа и выхода из JSON-поля
        login_logout_times = request.user.login_logout_times or {}
        
        # Найдите последнее время входа и добавьте к нему время выхода
        last_login_time = max(login_logout_times.keys())
        login_logout_times[last_login_time] = current_logout_time.isoformat()
        
        # Обновите JSON-поле
        request.user.login_logout_times = login_logout_times
        request.user.save()

        response = Response()
        response.delete_cookie('refresh')

        return response

    @action(methods=['DELETE'], detail=False, permission_classes=[IsAuthenticated], url_path=r'delete/(?P<id>.*)')
    def delete_user(self, request, id):
        if not id:
            return Response({'error': 'not put'})

        try:
            user = User.objects.get(id=id)
        except:
            return Response({'error': 'not put'})

        user.delete()
        return Response({'message': 'user delete'})
    