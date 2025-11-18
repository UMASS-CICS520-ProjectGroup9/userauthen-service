from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        })
        
        
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Override validate to check if the user is admin.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        # Check admin/staff permission
        if not self.user.is_staff and not self.user.is_superuser:
            raise serializers.ValidationError(
                {"detail": "Only admin users can log in here."}
            )

        # Add extra fields to the response if needed
        data["username"] = self.user.username
        data["is_staff"] = self.user.is_staff
        data["is_superuser"] = self.user.is_superuser

        return data


class AdminLoginView(TokenObtainPairView):
    serializer_class = AdminTokenObtainPairSerializer