from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', include('riego.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('riego.urls')),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),       # refresh token
]
