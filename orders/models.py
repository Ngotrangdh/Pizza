from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class ProductVariant(models.Model):
    SMALL = "sm"
    LARGE = "lg"
    ONESIZE = "os"
    SIZE_CHOICES = [(SMALL, "Small"), (LARGE, "Large"), (ONESIZE, "One Size")]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.CharField(max_length=64)
    topping_no = models.IntegerField(default=0)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=ONESIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    is_addon = models.BooleanField(default=False)

    def __str__(self):
        if self.is_addon:
            return f"{self.variant} - {self.size}"
        else:
            return f"{self.product} - {self.variant} - {self.get_size_display()}"


class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("r", "Received"),
        ("p", "Pendding"),
        ("d", "Done"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered_date = models.DateTimeField("Date Ordered")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="r")

    def __str__(self):
        return "Order %s - by %s at %s" % (
            self.id,
            self.user.username,
            self.ordered_date,
        )

    def get_total(self):
        total = 0
        items = OrderItem.objects.filter(order__id=self.id)
        for item in list(items):
            addon_total = 0
            for addon in item.addons.all():
                addon_total += addon.price
            total += item.item.price * item.quantity + addon_total
        return total

    def get_items(self):
        items = OrderItem.objects.filter(order__id=self.id)
        return list(items)


class OrderItem(models.Model):
    item = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="item"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping)
    addons = models.ManyToManyField(ProductVariant, related_name="addons")

    def __str__(self):
        return "Item %s" % (self.id)

    def get_unit_price(self):
        total_addon = 0
        for addon in self.addons.all():
            total_addon += addon.price
        return self.item.price + total_addon
