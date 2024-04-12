from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.hashers import check_password

class UserViewSets(viewsets.ModelViewSet):
    class_serializer = UserSerializer
    def signin(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        try:
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
        except User.DoesNotExist:
            detail = 'Authentication credentials are not correct.'
            return Response(data={'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if check_password(password, user.password):
            serializer = self.class_serializer(user, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            detail = 'Authentication credentials are not correct.'
            return Response(data={'detail': detail}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def logout(self, request):
        # Effacer le token côté client
        response = Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        response.delete_cookie("auth_token")
        return response
