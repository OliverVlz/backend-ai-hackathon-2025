from django.urls import path, include
from django.contrib import admin
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def root_view(request):
    return JsonResponse({'message': 'Bienvenido a la API de AiRiego!'}, status=200)

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/', include('riego.urls')),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
