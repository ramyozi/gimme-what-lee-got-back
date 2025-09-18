from django.contrib.auth import logout
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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
    """
    Attendre {"refresh": "<refresh_token>"} dans le body.
    Blackliste le refresh token pour empêcher la refresh flow.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# récupération des infos du compte connecté
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)
