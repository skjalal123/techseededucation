from Profile.models import *
from rest_framework.generics import UpdateAPIView
from rest_framework.viewsets import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .Serializers import *


class myProfile(ModelViewSet):
    queryset = myUser.objects.all()
    serializer_class = User
    lookup_field = "uid"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = myUser.objects.filter(id=self.request.user.id)
        return queryset

    def get_object(self):
        queryset = myUser.objects.get(id=self.request.user.id)
        return queryset


class Signup(ModelViewSet):
    queryset = myUser.objects.all()
    serializer_class = User


class ActivateUser(UpdateAPIView):
    # TODO activate user process
    pass
