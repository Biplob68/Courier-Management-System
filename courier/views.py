from django.shortcuts import render,redirect
from .models import Product,Order,OrderUpdate,Contact,Profile,Pending_order
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse,HttpResponseRedirect
from .forms import SignUpForm,ProfileForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
#from django.db.models import Q
from django.db.models import Sum
import datetime


pen_order = Pending_order.objects.all()
pen_param = {'orders': pen_order}

def index(request):
    return render(request, 'courier/index.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('fname','') + " " + request.POST.get('lname','')
        email = request.POST.get('email', '')
        desc = request.POST.get('description', '')
        phone = request.POST.get('mobile', '')
        cont = Contact(name=name,description=desc,email=email,phone=phone)
        cont.save()
    return render(request, 'courier/contact.html')

@login_required
def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        try:
            order = Order.objects.filter(order_id=orderId)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                most_update = OrderUpdate.objects.filter(order_id=orderId).all().last()
                params = {'updates': update, 'orderId': orderId,'most_update': most_update}
        except Exception as e:
            return HttpResponse('{}')
        return render(request, 'courier/tracker.html', params)
    return render(request, 'courier/tracker.html')


def order(request):
    products = Product.objects.all()
    params = {'product': products}
    if request.method == "POST":
        name = request.POST.get('s_name', '')
        email = request.POST.get('s_email', '')
        address = request.POST.get('s_address', '')
        phone = request.POST.get('s_phone', '')
        r_name = request.POST.get('r_name', '')
        r_email = request.POST.get('r_email', '')
        r_address = request.POST.get('r_address', '')
        r_phone = request.POST.get('r_phone', '')
        product = request.POST.get('product', '')
        weight = request.POST.get('weight','0.0')
        quantity = request.POST.get('quantity', '1.0')
        description = request.POST.get('other-info','')
        order1 = Order(sender_name=name, sender_email=email, sender_address=address,
                       sender_phone=phone,receiver_name=r_name,receiver_email=r_email,
                       receiver_address=r_address,receiver_phone=r_phone,weight=weight,
                       quantity=quantity,description=description,product_name=product)
        order1.save()
        update = OrderUpdate(order_id=order1.order_id,location="-------", update_desc="The order has been placed")
        update.save()

        pending = Pending_order(order_id=order1.order_id)
        pending.save()
        #thank = True
        id = order1.order_id
        return render(request, 'courier/thank.html', {'id': id})
    return render(request, 'courier/order.html',params)


def productView(request):
    products = Product.objects.all()
    params = {'product': products}
    return render(request, 'courier/product.html', params)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            u = User.objects.get(username=username)
            u1 = Profile.objects.get(user=u)
            if request.user.is_superuser or u1.user_type == 'Admin':
                return redirect('/admin')
            if u1.user_type == 'Customer':
                return redirect('/')
            else:
                return redirect('/emp_home')

    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'courier/signup.html', {'form': form , 'profile_form': profile_form})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        u = User.objects.get(username=username)
        u1 = Profile.objects.get(user=u)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.user.is_superuser or u1.user_type == 'Admin':
                   return redirect('/admin')
                if u1.user_type == 'Customer':
                    return redirect('/')
                if u1.user_type == 'Permitted_Employee':
                    return redirect('/emp_home')
                else:
                    return redirect('/')

            else:
                messages.error(request, 'Your account has been disabled..!')
                return render(request, 'courier/login.html')
        else:
            messages.error(request, 'Invalid login..!')
            return render(request, 'courier/login.html')
    else:
        return render(request, 'courier/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def emp_index(request):
    pen_order = Pending_order.objects.all()
    params = {'orders': pen_order}
    return render(request, 'courier/emp_index.html',params)


def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        return redirect('/login')
    else:
        return render(request,'courier/change_password.html')


def pending_order(request, order_id):
    #orders = OrderUpdate.objects.raw('SELECT UNIQUE  order_id FROM courier_orderupdate')
    pen_order = Pending_order.objects.all()
   # pending_order = Pending_order.objects.filter(order_id=order_id).all().last()
    pending_order_details = Order.objects.filter(order_id=order_id).all().last()
    params = {'orders': pen_order, 'pending_order_details': pending_order_details}
    return render(request, 'courier/pending_order.html', params)


def add_order(request):
    products = Product.objects.all()
    params = {'product': products,'orders': pen_order}
    if request.method == "POST":
        name = request.POST.get('s_name', '')
        address = request.POST.get('s_address', '')
        phone = request.POST.get('s_phone', '')
        r_name = request.POST.get('r_name', '')
        r_address = request.POST.get('r_address', '')
        r_phone = request.POST.get('r_phone', '')
        product_name = request.POST.get('product_name', '')
        weight = request.POST.get('weight','0.0')
        quantity = request.POST.get('quantity', '1.0')
        price = request.POST.get('price', '0.0')
        description = request.POST.get('other-info','')
        order1 = Order(sender_name=name, sender_address=address,
                       sender_phone=phone,receiver_name=r_name,
                       receiver_address=r_address,receiver_phone=r_phone,weight=weight,
                       quantity=quantity,description=description,price = price)
        order1.save()
        update = OrderUpdate(order_id=order1.order_id,location="-------", status="Picked-up")
        update.save()
        thank = True
        id = order1.order_id
        return render(request, 'courier/voucher.html', {'thank': thank, 'id': id, 'order': order1,'price': price, 'pro_name': product_name })
    else:
        return render(request,'courier/add_order.html',params)


def voucher(request):
    return render(request,'courier/voucher.html')


def update_order(request):
    if request.method == "POST":
        if 'search' in request.POST:
            search_input = request.POST['srh']
            if search_input:
                match = OrderUpdate.objects.filter(order_id=search_input).all().last()
                order2 = Order.objects.filter(order_id=search_input).all().last()
                if match:
                    return render(request, 'courier/update_order.html', {'search_result': match,'order':order2})
                else:
                    messages.error(request, 'No result found.')
        if 'update' in request.POST:
            location = request.POST.get('location', '')
            order_id = request.POST.get('order_id', '')
            status = request.POST.get('update_status', '')
            desc = request.POST.get('desc', '')
            price = request.POST.get('price', '0.0')
            if  price != 0.0:
                order1 = Order.objects.filter(order_id=order_id)
                for i in order1:
                    i.price = price
                    i.save()

            update = OrderUpdate(order_id=int(order_id), location=location, status=status,update_desc=desc)
            update.save()
            if status == 'Confirmed Order':
                instance = Pending_order.objects.get(order_id=order_id)
                instance.delete()
    return render(request,'courier/update_order.html',{'orders': pen_order})


def report(request):
    if request.method == "POST":
        report_date = request.POST.get('date', '')

        #r_order = OrderUpdate.objects.filter(time__year=y,time__month=m, time__day=d)
        order = OrderUpdate.objects.filter(time__date=report_date)
        total_placed = order.filter(status='Placed Order')
        total_picked = order.filter(status='Picked-up')
        total_reached = order.filter(status='Reached Product')
        total_delivered = order.filter(status='Delivered Product')

        total_pending = Pending_order.objects.filter(time__date=report_date)
        total_tk = Order.objects.filter(dateTime__date=report_date).aggregate(Sum('price'))['price__sum']
        params = {'total_pending':total_pending,'reporting_date':report_date,'total_placed':total_placed,
                  'total_picked':total_picked,'total_reached':total_reached,
                   'total_delivered':total_delivered,'total_tk': total_tk}
    return render(request,'courier/report.html',params,pen_param)


def thank(request):
    return render(request,'courier/thank.html')