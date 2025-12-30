from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, UserProfile
from .serializers import ProductSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination

# OTP Expiry Time (5 minutes)
OTP_EXPIRY_TIME = timedelta(minutes=5)

# -----------------------------
# Signup View
# -----------------------------
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_no = request.data.get('phone_no')
        business_name = request.data.get('business_name')
        login_type = request.data.get('login_type', 'email')  # Default to 'email'

        # Validate required fields
        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create the user profile with all fields
        user_profile = UserProfile.objects.create(
            user=user,
            phone_no=phone_no,
            business_name=business_name,
            is_verify=True,
            login_type=login_type
        )

        return Response({
            'message': 'User created successfully.',
            'user_id': user.id,
            'email': email
        }, status=status.HTTP_201_CREATED)


# -----------------------------
# Login View
# -----------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful!',
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'refresh': str(refresh),
                'access': access_token
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
# -----------------------------
# Product API View
# -----------------------------
class ApiProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        products = Product.objects.filter(user=request.user)
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        product_data = request.data.copy()
        product_data['user'] = request.user.id

        if Product.objects.filter(user=request.user, product_name=product_data['product_name']).exists():
            return Response({'error': 'You already have a product with this name.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully!',
                             'product': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Get the product ID from the query parameters
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert product_id to an integer
            product_id = int(product_id)

            # Ensure the product exists and belongs to the authenticated user
            product = Product.objects.get(id=product_id, user=request.user)
        except ValueError:
            return Response({'error': 'Invalid Product ID'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or you do not have permission to edit it.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the product with the provided data
        serializer = ProductSerializer(product, data=request.data, partial=True)  # Use partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully!',
                             'product': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = request.query_params.get('id')  # Get the product ID from the query parameters
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, user=request.user)  # Ensure the product belongs to the user
        except Product.DoesNotExist:
            return Response({'error': 'Product not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'message': 'Product deleted successfully!'}, status=status.HTTP_200_OK)

# -----------------------------
# transaction views
# -----------------------------
class ApiTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Implement logic to retrieve transactions for the authenticated user
        pass

    def post(self, request, *args, **kwargs):
        # Implement logic to create a new transaction for the authenticated user
        pass