from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone

from authentication.models import User
from authentication.serializers import UserSerializer
from office.models import Office
from role.models import Role


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        request.data['role'] = request.data.get('role') or 'User'
        request.data['office'] = Office.objects.get(id=request.data.get('office')).title

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
    def me(self, request):
        user = request.user
        data = self.serializer_class(user).data

        return Response(data)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        error = request.data.get('error')
        user = User.objects.get(id=request.user.id)

        # Получите текущее время выхода
        current_logout_time = timezone.now()
        
        # Получите существующие данные времени входа и выхода из JSON-поля
        login_logout_times = request.user.login_logout_times or {}
        
        # Найдите последнее время входа и добавьте к нему время выхода
        last_login_time = max(login_logout_times.keys(), default=0)
        login_logout_times[last_login_time] = {
            'logout_time': current_logout_time.isoformat(),
            'error': error
        }
        
        # Обновите JSON-поле
        setattr(user, 'login_logout_times', login_logout_times)
        user.save()

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
    
    @action(methods=['PATCH'], detail=False, permission_classes=[IsAdminUser], url_path='edit')
    def edit_user(self, request):
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        office = request.data.get('office')
        role = request.data.get('role')
        login_logout_times = request.data.get('login_logout_times')
        is_active = request.data.get('is_active')

        if email is None:
            raise ValidationError({ 'error': 'email must not be empty' })
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound({ 'error': 'user with this id was not found'})     

        if first_name: setattr(user, 'first_name', first_name)
        if last_name: setattr(user, 'last_name', last_name)
        if is_active is not None:
            user.is_active = is_active
        if office: setattr(user, 'office', Office.objects.get(title=office.get('title')))
        if role: setattr(user, 'role', Role.objects.get(title=role.capitalize()))
        if login_logout_times is not None: setattr(user, 'login_logout_times', login_logout_times)

        user.save()

        data = self.serializer_class(user).data

        return Response(data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAdminUser], url_path='users')
    def get_users(self, request):
        users = User.objects.all().exclude(email="admin@admin.com")

        data = UserSerializer(users, many=True).data

        return Response(data)
    
    @action(methods=['GET'], detail=False, permission_classes=[IsAdminUser], url_path=r'user/(?P<id>.*)')
    def get_user(self, request, id):
        user = User.objects.get(id=id)

        data = UserSerializer(user).data

        return Response(data)
