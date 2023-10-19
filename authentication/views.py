from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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

        if email is None:
            raise ValidationError({ 'error': 'email must not be empty' })
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound({ 'error': 'user with this id was not found'})     

        if first_name: setattr(user, 'first_name', first_name)
        if last_name: setattr(user, 'last_name', last_name)
        if office: setattr(user, 'office', office)
        if role: setattr(user, 'role', role)

        user.save()

        data = self.serializer_class(user).data

        return Response(data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAdminUser], url_path='users')
    def get_users(self, request):
        users = User.objects.all()

        data = UserSerializer(users, many=True).data

        return Response(data)
    
    @action(methods=['GET'], detail=False, permission_classes=[IsAdminUser], url_path=r'user/(?P<id>.*)')
    def get_user(self, request, id):
        user = User.objects.get(id=id)

        data = UserSerializer(user).data

        return Response(data)
