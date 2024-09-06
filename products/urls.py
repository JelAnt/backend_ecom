from django.urls import path
from .views import ComputerList, ComputerDetail

urlpatterns = [
path("<int:pk>/", ComputerDetail.as_view(), name="computer_detail"),
path("", ComputerList.as_view(), name="computer_list"),
]