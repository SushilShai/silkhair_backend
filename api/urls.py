from django.urls import path
from .views import SignupView, ApiProductView, LoginView, ApiTransactionView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products/', ApiProductView.as_view(), name='ApiProductView'),
    path('products/<int:product_id>', ApiProductView.as_view(), name='ApiProductView'),
    
    path('transactions/', ApiTransactionView.as_view(), name='ApiTransactionView'),
]