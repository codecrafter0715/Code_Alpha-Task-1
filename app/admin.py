from django.contrib import admin
from razorpay import Payment
from . models import Cart, Customer, OrderPlaced, Product, Payment

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment')
    search_fields = ('user__username', 'product__name', 'status')
    list_filter = ('status', 'ordered_date')
    ordering = ('-ordered_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_method', 'transaction_id', 'payment_status', 'paid', 'payment_date')
    search_fields = ('order_id', 'transaction_id', 'payment_method')
    list_filter = ('payment_status', 'payment_date')
    ordering = ('-payment_date',)

