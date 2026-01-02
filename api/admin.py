from django.contrib import admin
from .models import UserProfile, Category, Product, Transaction

# admin.site.register(UserProfile)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'user', 'category', 'unit_price', 'quantity')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_no', 'business_name', 'is_verify')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product', 'quantity', 'total_price', 'status', 'payment_method', 'transaction_date')
