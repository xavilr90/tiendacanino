from django.urls import path
from .views import index, listado_mascotas , mascota, comprar, grabar_mascotas
from . import views

urlpatterns = [
    path('',index),
    path('listado_mascotas/', listado_mascotas, name="listado_mascotas"),
    path('grabar_mascotas/', grabar_mascotas, name="grabar_mascotas"),
    path('<int:mascota_id>', mascota,name='mascota'),
    path('<int:mascota_id>/comprar', comprar,name='comprar'),
    path('signup/', views.signup, name='signup'),
    path('signup_register/', views.signup)
]