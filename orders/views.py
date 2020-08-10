from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product, ProductVariant, Topping, Order, OrderItem
import random, string


class ProductVariantView:
    def __init__(
        self, variant, topping_no, small, large, onesize, is_addon, modal_name
    ):
        self.variant = variant
        self.topping_no = topping_no
        self.small = small
        self.large = large
        self.onesize = onesize
        self.is_addon = is_addon
        self.modal_name = modal_name

    def __str__(self):
        return f"{self.variant} - {self.onesize} - {self.small} - {self.large}"


class VariantPriceView:
    def __init__(self, id, price):
        self.id = id
        self.price = price


class ProductView:
    def __init__(self, name):
        self.name = name
        self.variants = []

    def add_variant(self, variant):
        self.variants.append(variant)

    def is_one_size(self):
        if len(self.variants) == 0:
            return True
        return self.variants[0].onesize != None

    def is_pizza(self):
        return "Pizza" in self.name

    def is_sub(self):
        return "Sub" in self.name


class Cart:
    def __init__(self, user):
        self.user = user
        self.items = []

    def addItem(self, item):
        existing_items = [
            i
            for i in self.items
            if i.variant.id == item.variant.id and i.toppings == item.toppings
        ]
        if len(existing_items) > 0:
            existing_items[0].quantity += 1
        else:
            self.items.append(item)

    def getTotal(self):
        total = sum(i.quantity for i in self.items)
        return total

    def getTotalPrice(self):
        total = sum(i.quantity * float(i.variant.price) for i in self.items)
        return total


class CartItem:
    def __init__(self, variant_id, topping_ids, addon_ids):
        self.variant = ProductVariant.objects.get(pk=variant_id)
        self.toppings = [
            topping for topping in Topping.objects.filter(pk__in=topping_ids)
        ]
        self.addons = [
            addon for addon in ProductVariant.objects.filter(pk__in=addon_ids)
        ]
        self.quantity = 1

    def unit_price(self):
        total_addon = 0
        for addon in self.addons:
            total_addon += addon.price
        return self.variant.price + total_addon


shopping_carts = {}


@login_required
def index(request):
    user = request.user
    product_name_list = []
    product_view_list = []

    productVariants = ProductVariant.objects.all()
    # get product
    for product in Product.objects.all():
        product_name = product.name

        if product_name in product_name_list:
            continue

        product_view = ProductView(product_name)
        variant_view_list = []

        # get variant
        for productVariant in productVariants:
            if productVariant.product.name == product_name:
                variant_name = productVariant.variant
                topping_no = productVariant.topping_no
                is_addon = productVariant.is_addon

                if variant_name in variant_view_list:
                    continue

                small_price = None
                large_price = None
                onesize_price = None
                modal_name = "#nonPizzaToppingModal"

                # get size
                for productVariant in productVariants:
                    if (
                        productVariant.product.name == product_name
                        and productVariant.variant == variant_name
                    ):
                        variant_id = productVariant.id
                        size = productVariant.size

                        if size == "sm":
                            small_price = VariantPriceView(
                                variant_id, productVariant.price
                            )

                        elif size == "lg":
                            large_price = VariantPriceView(
                                variant_id, productVariant.price
                            )
                        else:
                            onesize_price = VariantPriceView(
                                variant_id, productVariant.price
                            )

                        if product_view.is_pizza():
                            modal_name = "#pizzaToppingModal"
                        elif product_view.is_sub():
                            modal_name = "#subModal"

                    if (
                        small_price != None and large_price != None
                    ) or onesize_price != None:
                        break

                variant = ProductVariantView(
                    variant_name,
                    topping_no,
                    small_price,
                    large_price,
                    onesize_price,
                    is_addon,
                    modal_name,
                )

                variant_view_list.append(variant_name)
                product_view.add_variant(variant)

        product_name_list.append(product_name)
        product_view_list.append(product_view)

    topping_list = Topping.objects.all()
    cart = shopping_carts.get(request.user.id)
    if cart != None:
        total_items = cart.getTotal()
    else:
        total_items = 0

    context = {
        "products": product_view_list,
        "toppings": topping_list,
        "total_items": total_items,
    }
    return render(request, "orders/index.html", context)


@login_required
def add_to_cart(request):
    variant_id = request.POST.get("id", None)
    toppings = request.POST.get("toppings", None)
    topping_ids = [int(float(i)) for i in toppings.split(",")] if toppings else []
    addons = request.POST.get("addons", None)
    addon_ids = [int(float(i)) for i in addons.split(",")] if addons else []

    try:
        variant = ProductVariant.objects.get(pk=variant_id)
    except ProductVariant.DoesNotExist:
        raise Http404("Item does not exist")

    # validate number of toppings
    if len(topping_ids) != ProductVariant.objects.get(pk=variant_id).topping_no:
        raise Http404("Item does not exist")

    cart = shopping_carts.get(request.user.id)
    if cart == None:
        cart = Cart(request.user)
        shopping_carts[request.user.id] = cart

    item = CartItem(variant_id, topping_ids, addon_ids)
    cart.addItem(item)
    messages.success(
        request,
        f"{item.variant.product} - {item.variant.variant} has been added to your shopping cart",
    )

    return JsonResponse({"total": cart.getTotal()})


@login_required
def update_item_quantity(request):
    variant_id = request.POST.get("id", None)
    quantity = request.POST.get("quantity", None)
    cart = shopping_carts.get(request.user.id)
    updated_item = [item for item in cart.items if item.variant.id == int(variant_id)]
    updated_item[0].quantity = int(quantity)
    messages.success(
        request, f"Your shopping cart has been updated!",
    )

    return HttpResponse(status=204)


@login_required
def delete_cart(request):
    variant_id = request.POST.get("id", None)
    cart = shopping_carts.get(request.user.id)
    deleted_item = [item for item in cart.items if item.variant.id == int(variant_id)]
    cart.items.remove(deleted_item[0])
    messages.success(
        request, f"Successfully remove the item from cart!",
    )
    return HttpResponse(status=204)


@login_required
def get_cart(request):
    cart = shopping_carts.get(request.user.id)
    if cart == None:
        items = []
        total_items = 0
        total_price = 0
    else:
        items = cart.items
        total_items = cart.getTotal()
        total_price = cart.getTotalPrice()

    context = {"items": items, "total": total_price, "total_items": total_items}
    return render(request, "orders/cart.html", context)


@login_required
def place_order(request):
    cart = shopping_carts.get(request.user.id)
    # Insert order to database
    if cart == None:
        return HttpResponse("There's no items in your cart")
    else:
        ref_code = create_ref_code()
        new_order = Order.objects.create(
            user=request.user, ref_code=ref_code, ordered_date=timezone.now()
        )
        for item in cart.items:
            order_item = OrderItem.objects.create(
                item=item.variant, order=new_order, quantity=item.quantity
            )
            for topping in item.toppings:
                t = Topping.objects.get(pk=topping.id)
                order_item.toppings.add(t)
            for addon in item.addons:
                addon_variant = ProductVariant.objects.get(pk=addon.id)
                order_item.addons.add(addon_variant)

        shopping_carts.pop(request.user.id)
        messages.success(
            request,
            f"Your order has been received and will be processed as soon as possible",
        )

    return HttpResponseRedirect(reverse("order_summary", args=(new_order.id,)))


@login_required
def order_summary(request, order_id):
    items = OrderItem.objects.filter(order__user=request.user, order__id=order_id)
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    total = order.get_total()
    ref_code = order.ref_code
    cart = shopping_carts.get(request.user.id)
    if cart == None:
        total_items = 0
    else:
        total_items = cart.getTotal()
    context = {
        "items": list(items),
        "total": total,
        "total_items": total_items,
        "ref_code": ref_code,
    }
    return render(request, "orders/order.html", context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    cart = shopping_carts.get(request.user.id)
    if cart == None:
        total_items = 0
    else:
        total_items = cart.getTotal()
    context = {"orders": list(orders), "total_items": total_items}
    return render(request, "orders/history.html", context)


def create_ref_code():
    return "".join(random.choices((string.ascii_lowercase + string.digits), k=10))
