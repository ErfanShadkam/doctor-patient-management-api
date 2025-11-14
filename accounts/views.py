from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .filters import UserRoleFilter
from .models import User
from .serializers import UserSerializer, MakeDoctorSerializer
from rest_framework.permissions import AllowAny,IsAdminUser


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserRoleFilter

    @action(detail=True, methods=['post'],serializer_class=MakeDoctorSerializer)
    def make_doctor(self, request, pk=None):
        user = self.get_object()
        user.is_doctor = True
        user.is_patient = False
        user.save()
        return Response({"message": f"{user.username} is now a doctor."})
    
    
