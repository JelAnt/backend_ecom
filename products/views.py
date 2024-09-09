from rest_framework import generics, permissions
from .serializers import ComputerSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Computer

class ComputerList(generics.ListCreateAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ComputerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer