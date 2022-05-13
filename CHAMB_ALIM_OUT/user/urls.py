from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('password_reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('coord/', views.UserCoordView.as_view(), name='coord'),
]
