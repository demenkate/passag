from django.contrib import admin

from carts.models import Cart



class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "sizeproduct", "quantity", "created_timestamp"
    search_fields = "sizeproduct", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user_display", "sizeproduct_display", "quantity", "created_timestamp",]
    list_filter = ["created_timestamp", "user", "sizeproduct__product__name",]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def sizeproduct_display(self, obj):
        return str(obj.sizeproduct.product.name)