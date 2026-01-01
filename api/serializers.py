from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, Product, Transaction

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_no', 'name']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'user', 'product_name', 'category', 'sku', 'unit_price', 'quantity', 'description']

class TransactionSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()  # Display product name instead of ID

    class Meta:
        model = Transaction
        fields = [
            'id',
            'customer',
            'email',
            'product',
            'quantity',
            'total_price',
            'status',
            'transaction_date',
            'payment_method'
        ]
        read_only_fields = ['id', 'transaction_date']