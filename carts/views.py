from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from django.forms import ValidationError
from django.contrib import messages

from goods.models import Products, SizeProductRelation


def cart_add(request):
    sizeproduct_id = request.POST.get("product_id")
    print(sizeproduct_id)

    sizeproduct = SizeProductRelation.objects.get(id=sizeproduct_id)
    # product = Products.objects.get(id=sizeproduct_id)
    print(sizeproduct)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, sizeproduct=sizeproduct)

        if carts.exists():

            cart = carts.first()
            if cart:
                if sizeproduct.count == cart.quantity:
                    print('ошибка')
                    messages.error(request, 'Недостаточное количество товара на складе\
                                           В наличии - {sizeproduct.count}')
                    raise ValidationError(f'Недостаточное количество товара на складе\
                                           В наличии - {sizeproduct.count}')
                else:
                    cart.quantity += 1
                    cart.save()
        else:
            Cart.objects.create(user=request.user, sizeproduct=sizeproduct, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, sizeproduct=sizeproduct)

        if carts.exists():
            cart = carts.first()
            if cart:
                if sizeproduct.count == cart.quantity:
                    response_data = {
                        "message": f'Недостаточное количество товара на складе\
                                           В наличии - {sizeproduct.count}',
                    }

                    return JsonResponse(response_data)
                else:
                    cart.quantity += 1
                    cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, sizeproduct=sizeproduct, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    print(quantity)

    cart = Cart.objects.get(id=cart_id)

    if int(quantity) > cart.sizeproduct.count:
        raise ValidationError(f'Недостаточное количество товара на складе\
                                                   В наличии - {cart.sizeproduct.count}')
    else:

        cart.quantity = quantity
        cart.save()
        updated_quantity = cart.quantity

    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart}, request=request)

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
        "quaantity": updated_quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    print(quantity)
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "message": "Товар удален",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)