from django.contrib import admin
from .models import Product, ProductVariant, Topping, Order, OrderItem
from django.utils.html import format_html_join, format_html


# Register your models here.
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductVariantInline,
    ]


class OrderItemInline(admin.TabularInline):
    readonly_fields = ["item", "quantity", "toppings", "addons"]
    model = OrderItem
    extra = 0

    def toppings(self, instance):
        return format_html_join(
            "{},", (topping.name for topping in list(instance.toppings.all()))
        )

    def addons(self, instance):
        return format_html_join(
            "{},", (addon.variant for addon in list(instance.addons.all()))
        )


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "user", "ordered_date"]
    inlines = [
        OrderItemInline,
    ]

    actions = ["make_pendding", "make_done"]

    def make_pendding(self, request, queryset):
        rows_updated = queryset.update(status="p")
        if rows_updated == 1:
            message_bit = "1 order was"
        else:
            message_bit = "%s orders were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    def make_done(self, request, queryset):
        rows_updated = queryset.update(status="p")
        if rows_updated == 1:
            message_bit = "1 order was"
        else:
            message_bit = "%s orders were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    make_pendding.short_description = "Mark selected orders as pending"
    make_done.short_description = "Mark selected orders as done"


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)
