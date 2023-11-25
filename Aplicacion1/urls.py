from django.urls import include, path
from .views import iniciodesesion, register, inicio, cuestionario, psd, resultadospregunta
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',iniciodesesion,name="iniciodesesion"),
    path('login/',LoginView.as_view(),name="login_url"),
    path('register/',register,name="register_url"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('inicio/',inicio,name="inicio"),
    path('cuestionario/',cuestionario,name="cuestionario_url"),
    path('psd/',psd,name="psd_url"),
    path('retroalimentacion/<int:prespondida_pk>/',resultadospregunta,name="retroalimentacion_url"),
]