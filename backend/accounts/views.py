from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': '회원가입이 완료되었습니다.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': '아이디와 비밀번호를 입력해주세요.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 클라이언트에서 토큰을 삭제하는 방식으로 처리
        return Response({'message': '로그아웃 되었습니다.'})


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UserManageView(APIView):
    """슈퍼유저 전용: 유저 목록 조회 및 스태프 권한 부여/해제"""
    permission_classes = [IsSuperUser]

    def get(self, request):
        users = User.objects.all().order_by('id')
        return Response(UserSerializer(users, many=True).data)

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '유저를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_superuser:
            return Response({'error': '슈퍼유저의 권한은 변경할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        is_staff = request.data.get('is_staff')
        if is_staff is not None:
            user.is_staff = bool(is_staff)
            user.save()

        return Response(UserSerializer(user).data)
