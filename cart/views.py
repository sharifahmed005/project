import json
from django.http import JsonResponse
from product.models import Order, OrderItem, Payment, Product, ShippingAddress
from django.shortcuts import get_object_or_404, redirect, render

import datetime
# Create your views here.


def cart_summery(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    context = {'items': items, 'order': order}
    return render(request, 'cart/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
       
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
    



    context = {'items': items, 'order': order}
    return render(request, 'cart/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Product Id: ', productId)
    print('Action: ', action)

    customer = request.user
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    # order = Order.objects.create(
    #     customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'remove_item':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item Was Added.', safe=False)



def updateOrder(request):
    if request.method == 'POST':
        print(request.POST['total'])
        print(request.POST['quantity'])
   
        customer = request.user
        order = Order.objects.get(
                customer=customer, complete=False)
        order.total = request.POST['total']

        order.tax = request.POST['tax']
        order.gtotal = int(float(request.POST['tax'])) + int(float(request.POST['total']))
        order.quantity = request.POST['quantity']
        order.save()
        return redirect('checkout')



def processOrder(request):
    if request.user.is_authenticated:
       if request.method == 'POST':
            tr_id = request.POST['tr_id']

            customer = request.user
            order = Order.objects.get(
                customer=customer, complete=False)

            order.transaction_id = tr_id
            order.save()
        
            ac_name = request.POST['ac_name']
            ac_number = request.POST['ac_number']
            address = request.POST['address']
            Payment.objects.create(ac_name=ac_name, ac_number=ac_number, tr_id=tr_id)
            
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=address
            )




    return redirect('purchase_history')




def purchase_history(request):
    user = request.user
    order = Order.objects.filter(customer=user, complete=True)
    orderItem = OrderItem.objects.all()

    if request.GET:
        id = request.GET['order_id']
        orders = Order.objects.get(id=id)
        orders.cancel = True 
        orders.save()

    context = {
        'items': orderItem,
        'order': order
    }
    print(context)
    return render(request, 'cart/purchase.html', context)

