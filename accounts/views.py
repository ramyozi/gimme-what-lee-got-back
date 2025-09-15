from django.contrib.auth import logout
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Account
from accounts.serializers.read import AccountSerializer
from accounts.serializers.write import RegisterSerializer


# login JWT standard
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# création d'utilisateur avec vérification des rôles
class RegisterView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# logout / déconnexion
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        logout(request)

# récupération des infos du compte connecté
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)
