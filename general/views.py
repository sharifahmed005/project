from io import BytesIO
from django.db.models import Q
from django.http.response import HttpResponse
from general.models import Message, Subscriber
from django.shortcuts import redirect, render
from django.core.mail import send_mail
# Create your views here.
from account.models import User
from product.models import Order, OrderItem, Product
from product.views import productview
from xhtml2pdf import pisa
from django.template.loader import get_template


def home(request):
    products = Product.objects.all().order_by('-id')[0:3]
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    context = {'order': order, 'products': products}
    return render(request, 'index.html', context)


def about(requets):
    return render(requets, 'about.html')


def contact(request):

    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(subject, message,
                  email, ['test@gmail.com'], fail_silently=False)

        return render(request, 'contact.html', {'message': "Mail Sent Successfully"})

    return render(request, 'contact.html')


def subscriber(request):

    if request.method == 'POST':
        email = request.POST['subscriber']
        Subscriber.objects.create(email=email)

        return redirect('home')


def agreeculturist(request):
    agreeculturists = User.objects.filter(
        Q(user_type='VATONARIS') | Q(user_type='AGRICULTURERIST'))
    context = {
        'agreeculturists': agreeculturists
    }
    return render(request, 'agriculturerist.html', context)


def message_farmer(request, id):
    message = Message.objects.filter(expart=id).filter(farmer=request.user.id)
    expart = User.objects.get(id=id)
    farmer = User.objects.get(id=request.user.id)
    if(request.POST):
        if(request.FILES):
            Message.objects.create(
                expart=expart, farmer=farmer, image=request.FILES['image'], message=request.POST['message'])
        else:
            Message.objects.create(
                expart=expart, farmer=farmer, message=request.POST['message'])
    else:
        Message.objects.filter(
            farmer=request.user.id, expart=id).update(seen=True)

    context = {
        'messages': message,
        'id': id
    }
    return render(request, 'message.html', context)


def sms_farmar(request):
    message = Message.objects.filter(
        farmer=request.user.id).filter(reply=True).order_by('-id')

    context = {
        'messages': message,
    }
    return render(request, 'sms.html', context)


def message_list(request):
    message = Message.objects.filter(
        expart=request.user.id).filter(reply=False).order_by('-id')

    context = {
        'messages': message,
    }
    return render(request, 'message_list.html', context)


def message_expart(request, id):
    farmers = User.objects.filter(
        user_type='FARMAR').filter(is_staff=False)
    far_user = Message.objects.filter(expart=request.user.id)
    message = Message.objects.filter(expart=request.user.id).filter(farmer=id)
    expart = User.objects.get(id=request.user.id)
    farmer = User.objects.get(id=id)
    if(request.POST):
        if(request.FILES):
            Message.objects.create(
                expart=expart, farmer=farmer, image=request.FILES['image'], reply='True', message=request.POST['message'])
        else:
            Message.objects.create(
                expart=expart, farmer=farmer, reply='True', message=request.POST['message'])
    else:
        Message.objects.filter(
            farmer=id, expart=request.user.id).update(seen=True)

    context = {
        'farmers': farmers,
        'fars': far_user,
        'messages': message,
        'id': id
    }
    return render(request, 'message_reply.html', context)


def terms(request):
    return render(request, 'termsofservice.html')


def privacy(request):
    return render(request, 'privacypolicy.html')


def order(request):
    order = Order.objects.filter(
        complete=True).filter(customer=request.user.id)
    context = {
        'orders': order
    }
    return render(request, 'order.html', context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def report(request):
    report = Order.objects.filter(
        complete=True).filter(customer=request.user.id)

    for key in report:
        data = {
            'username': key.customer,
            'transaction_id': key.transaction_id,
            'total':key.total,
            'quantity':key.quantity,
            'tax': key.tax,
            'gtotal': key.gtotal,
            'date': key.date_orderd,
            
        }
    pdf = render_to_pdf('report_pdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


