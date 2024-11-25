from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('listado_mascotas/', views.listado_mascotas, name="listado_mascotas"),
    path('grabar_mascotas/', views.grabar_mascotas, name="grabar_mascotas"),
    path('<int:mascota_id>', views.mascota,name='mascota'),
    path('<int:mascota_id>/comprar', views.comprar,name='comprar'),
    path('signup/', views.signup, name='signup'),
    path('signup_register/', views.signup),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    
    ]