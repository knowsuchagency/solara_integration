from django.urls import path
from . import views

urlpatterns = [
    path('jupyter/api/kernels/<str:id>/', views.kernels, name='kernels'),
    path('jupyter/api/kernels/<str:kernel_id>/<str:name>/', views.kernels_connection, name='kernels_connection'),
    path('_solara/api/close/<str:kernel_id>/', views.close, name='close'),
    path('static/public/<path:path>/', views.public, name='public'),
    path('static/assets/<path:path>/', views.assets, name='assets'),
    path('static/nbextensions/<str:dir>/<str:filename>/', views.nbext, name='nbext'),
    path('static/<path:path>/', views.serve_static, name='serve_static'),
    path('cdn/<path:path>/', views.cdn, name='cdn'),
    path('', views.read_root, name='read_root'),
    path('readyz/', views.readyz, name='readyz'),
]
