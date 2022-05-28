from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from user import views


app_name = 'user'

# create_chefelev création chef_elev avec tel
# me modification tout sauf tel ne peut-être fait que par le titulaire du compte
# modification tel et adresse à venir ne peut-être fait que par le titulaire du compte

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('me/', views.ManageUserView.as_view(),
         name='me'),
    path('coord/', views.UserCoordView.as_view(), name='coord'),
]
