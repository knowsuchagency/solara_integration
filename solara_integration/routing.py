from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('jupyter/api/kernels/<str:kernel_id>/<str:name>/', consumers.KernelConsumer.as_asgi()),
]
