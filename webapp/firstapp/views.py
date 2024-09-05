from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
import string
import random
from datetime import datetime


# Create your views here.
def Home(request):
    return render(request, 'firstapp/home.html')

def TrackingPage(request):
    tracks = Tracking.objects.all()
    context = {'tracks':tracks}
    return render(request, 'firstapp/tracking.html', context)

def Contact(request):
    return render(request, 'firstapp/contact.html')

def Ask(request):
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        email = data.get('email')
        title = data.get('title')
        detail = data.get('detail')

        new = AskQA()
        new.name = name
        new.email = email
        new.title = title
        new.detial = detail
        new.save()

    return render(request, 'firstapp/ask.html')

@login_required
def Questions(request):
    questions = AskQA.objects.all()
    context = {'questions':questions}
    return render(request, 'firstapp/questions.html', context)

@login_required
def Answer(request, askid):
    record = AskQA.objects.get(id=askid)
    if request.method == 'POST':
        data = request.POST.copy()
        detail_answer = data.get('detail_answer')
        record.detail_answer = detail_answer
        record.save()
    context = {'record':record}
    return render(request, 'firstapp/answer.html', context)

def Posts(request):
    posts = Post.objects.all().order_by('id').reverse()[:3]
    context = {"posts": posts}
    return render(request, 'firstapp/blogs.html', context)

def PostDetail(request, slug):
    posts = Post.objects.all().order_by('id').reverse()[:3]
    try: 
        single_post = get_object_or_404(Post, slug=slug)
        print("รายละเอียด", single_post)
    except Post.DoesNotExist:
        return render(request, 'firstapp/home.html')
    context = {"single_post":single_post, "posts":posts}
    return render(request, 'firstapp/blog-detail.html', context)

def Register(request):

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        check = User.objects.filter(username=email)
        
        if len(check) == 0:

            newuser = User()
            newuser.username = email
            newuser.first_name = name
            newuser.set_password(password)
            newuser.save()

            profile = Profile()
            profile.user = newuser
            profile.save()

            context['success'] = 'success'
        else:
            context['usertaken'] = 'usertaken'

    return render(request, 'firstapp/register.html', context)


def Login(request):

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        email = data.get('email')
        password = data.get('password')

        check = User.objects.filter(username=email)
        
        if len(check) == 0:

            context['nouser'] = 'nouser'

        else:
            try:
                user = authenticate(username=email,password=password)
                login(request,user)
                return redirect('questions')
            except:
                context['wrongpassword'] = 'wrongpassword'

    return render(request, 'firstapp/login.html', context)

def AllProduct(request):
    all_product = Product.objects.filter(available=True)
    # print("All Product", all_product)
    context = {"all_product" : all_product}

    return render(request, "firstapp/all-product.html", context)

def DiscountPage(request):

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        check = data.get('discount')
        if check == 'check-true':
            user = User.objects.get(username=request.user.username)
            discount = Discount.objects.get(user=user)
            discount.active = True
            discount.save()
            return redirect('all-product')
        
    return render(request, 'firstapp/discount.html', context)

def RandomOrderID():
    ro_id = ""
    ro_id += random.choice(string.ascii_uppercase)
    ro_id += random.choice(string.ascii_uppercase)

    for i in range(8):
        ro_id += random.choice("0123456789")
    
    return ro_id


def ProductDetail(request, slug):

    RandomOrderID()

    product = Product.objects.get(slug=slug)
    context = {"product": product, "product_price": product.normal_price}

    if product.price1 > 0:
        price_1 = (product.price1 * 100) / product.normal_price

        context["price_1"] = 100 - int(price_1)
        context["product_price"] = product.price1
    if product.price2 > 0:
        price_2 = (product.price2 * 100) / product.normal_price

        context["price_2"] = 100 - int(price_2)

    if request.method == "POST":
        data = request.POST.copy()

        new_order = Order()
        # new_order.user = product
        new_order.products = product
        new_order.first_name = data.get("first_name")
        new_order.last_name = data.get("last_name")
        new_order.tel = data.get("tel")
        new_order.email = data.get("email")
        new_order.address = data.get("address")
        new_order.count = data.get("count")
        new_order.buyer_price = data.get("buyer_price")
        new_order.shipping_cost = data.get("shipping_cost")
        
        try:
            file_image = request.FILES["upload_slip"]
            file_image_name = request.FILES["upload_slip"].name.replace(" ", "")
            file_system_storage = FileSystemStorage()
            file_name = file_system_storage.save(
                "products-slip/" + file_image_name, file_image
            )
            upload_file_url = file_system_storage.url(file_name)
            new_order.slip = upload_file_url[6:]
        except:
            new_order.slip = "/default.png"

        new_order.save()

        # เพิ่ม function random id 
        try:
            tracking_id = TrackingOrderID.objects.all()
            while True:
                order_ID = RandomOrderID()
                for tid in tracking_id:
                    if order_ID == tid.order_id:
                        continue
                break
        except:
            order_ID = RandomOrderID()

        new_tracking_id = TrackingOrderID()
        new_tracking_id.tracking_order = new_order
        new_tracking_id.order_id = order_ID
        new_tracking_id.save()

        return redirect("tracking-order-id-page", order_ID)

    return render(request, "firstapp/product-detail.html", context)

def TrackingOrderId(request, tid):
    tracking_id = TrackingOrderID.objects.get(order_id=tid).tracking_order
    buyer_price = tracking_id.buyer_price

    if buyer_price == int(buyer_price):
        buyer_price = int(buyer_price)

    shipping_cost = tracking_id.shipping_cost
    if shipping_cost == int(shipping_cost):
        shipping_cost = int(shipping_cost)

    all_price = tracking_id.buyer_price + tracking_id.shipping_cost

    context = {
        "tracking_id": tracking_id,
        "buyer_price": buyer_price,
        "order_id":tid,
        "shipping_cost":shipping_cost,
        "all_price":all_price
    }

    return render(request, "firstapp/tracking-order.html", context)

def AddToCart(request, pid):
    username = request.user.username
    user = User.objects.get(username=username)
    check = Product.objects.get(id=pid)

    try:
        new_cart = Cart.objects.get(user=user, product_id=str(pid))
        new_quantity = new_cart.quantity + 1
        new_cart.quantity = new_quantity
        calculate = new_cart.price * new_quantity
        new_cart.total = calculate
        new_cart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])

        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()

        return redirect('all-product')

    except:
        new_cart = Cart()
        new_cart.user = user
        new_cart.product_id = pid
        new_cart.product_name = check.name
        new_cart.price = int(check.normal_price)
        new_cart.quantity = 1
        calculate = int(check.normal_price) * 1
        new_cart.total = calculate
        new_cart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()

        return redirect('all-product')



def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        product_id = data.get('product_id')

        try:
            item = Cart.objects.get(user=user, product_id=product_id)
            item.delete()
            context['status'] = 'delete'
        except Cart.DoesNotExist:
            item = None

    count = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in count])
    updated_quantity = Profile.objects.get(user=user)
    updated_quantity.cart_quantity = count
    updated_quantity.save()

    mycart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in mycart])
    total = sum([c.total for c in mycart])

    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total

    return render(request, "firstapp/my-cart.html", context)

def MyCartEdit(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == "POST":
        data = request.POST.copy()
        if data.get("clear") == "clear":
            Cart.objects.filter(user=user).delete()
            updated_quantity = Profile.objects.get(user=user)
            updated_quantity.cart_quantity = 0
            updated_quantity.save()
            return redirect("my-cart")

        edit_list = []
        for k, v in data.items():
            if k[:2] == "pd":
                pid = int(k.split("_")[1])
                dt = [pid, int(v)]
                edit_list.append(dt)
        for ed in edit_list:
            edit_cart = Cart.objects.get(product_id=ed[0], user=user)
            edit_cart.quantity = ed[1]
            calculate = edit_cart.price * ed[1]
            edit_cart.total = calculate
            edit_cart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updated_quantity = Profile.objects.get(user=user)
        updated_quantity.cart_quantity = count
        updated_quantity.save()

        return redirect("my-cart")
    
    mycart = Cart.objects.filter(user=user)
    context["mycart"] = mycart
    return render(request, "firstapp/my-cart-edit.html", context)

def Checkout(request):
    username = request.user.username
    user = User.objects.get(username=username)

    if request.method == "POST":
        data = request.POST.copy()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        tel = data.get("tel")
        email = data.get("email")
        address = data.get("address")
        express = data.get("express")
        payment = data.get("payment")
        other = data.get("other")
        page = data.get("page")

        if page == "information":
            context = {}
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['tel'] = tel
            context['email'] = email
            context['address'] = address
            context['express'] = express
            context['payment'] = payment
            context['other'] = other

            mycart = Cart.objects.filter(user=user)
            count = sum([c.quantity for c in mycart])
            total = sum([c.total for c in mycart])

            context["mycart"] = mycart
            context["count"] = count
            context["total"] = total

            return render(request, "firstapp/checkout-confirm.html", context)
        
        if page == "confirm":
            mycart = Cart.objects.filter(user=user)
            member_id = str(user.id).zfill(4)
            date_time = datetime.now().strftime("%Y%m%d%H%M%S")
            order_id = "OD" + member_id + date_time

            for mc in mycart:
                cart_order = OrderProduct()
                cart_order.order_id = order_id
                cart_order.product_id = mc.product_id
                cart_order.product_name = mc.product_name
                cart_order.price = mc.price
                cart_order.quantity = mc.quantity
                cart_order.total = mc.total
                cart_order.save()

            new_order = CartOrder()
            new_order.order_id = order_id
            new_order.user = user
            new_order.first_name = first_name
            new_order.last_name = last_name
            new_order.tel = tel
            new_order.email = email
            new_order.address = address
            new_order.express = express
            new_order.payment = payment
            new_order.other = other
            new_order.save()

            Cart.objects.filter(user=user).delete()
            updated_quantity = Profile.objects.get(user=user)
            updated_quantity.cart_quantity = 0
            updated_quantity.save()

            return redirect("upload-slip-order", order_id=order_id)
        
    return render(request, "firstapp/checkout.html")

def CartOrderProduct(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    cart_order = CartOrder.objects.filter(user=user)

    for co in cart_order:
        order_id = co.order_id

        order_product = OrderProduct.objects.filter(order_id=order_id)

        total = sum([o.total for o in order_product])
        co.total = total
        count = sum([o.quantity for o in order_product])

        if co.express == "flash":
            shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
        elif co.express == "kerry":
            shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
        elif co.express == "j&t":
            shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
        elif co.express == "thailandpost":
            shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
        else:
            shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

        if co.payment =="cod":
            shipping_cost += 10
        co.shipping_cost = shipping_cost

    context["cart_order"] = cart_order

    return render(request, "firstapp/cart-order-product.html", context)

def UploadSlipOrder(request, order_id):
    if request.method == "POST" and request.FILES["upload_slip"]:
        data = request.POST.copy()

        slip_time = data.get("slip_time")
        bank_account = data.get("bank_account")

        updated_cart_order = CartOrder.objects.get(order_id=order_id)
        updated_cart_order.slip_time = slip_time
        updated_cart_order.bank_account = bank_account

        file_image_slip = request.FILES["upload_slip"]
        file_image_name = request.FILES["upload_slip"].name.replace(" ", "")
        file_system_storage = FileSystemStorage()
        file_name = file_system_storage.save(file_image_name, file_image_slip)
        upload_file_url = file_system_storage.url(file_name)
        updated_cart_order.slip = upload_file_url[6:]

        updated_cart_order.save()

    order_product = OrderProduct.objects.filter(order_id=order_id)
    total = sum([o.total for o in order_product])
    cart_order_detail = CartOrder.objects.get(order_id=order_id)
    count = sum([o.quantity for o  in order_product])
         
    if cart_order_detail.express == "flash":
        shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
    elif cart_order_detail.express == "kerry":
        shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
    elif cart_order_detail.express == "j&t":
        shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
    elif cart_order_detail.express == "thailandpost":
        shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

    if cart_order_detail.payment == "cod":
        shipping_cost += 10

    context = {
        "order_id": order_id,
        "total": total,
        "shipping_cost": shipping_cost,
        "grand_total": total + shipping_cost,
        "cart_order_detail": cart_order_detail,
        "count": count
    }

    return render(request, "firstapp/upload-slip-order.html", context)

def CustomerAllOrder(request):
    context = {}
    cart_order = CartOrder.objects.all().order_by("-id")

    for co in cart_order:
        order_id = co.order_id
        order_product = OrderProduct.objects.filter(order_id=order_id)
        total = sum([o.total for o in order_product])
        co.total = total
        count = sum([o.quantity for o in order_product])

        if co.express == "flash":
            shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
        elif co.express == "kerry":
            shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
        elif co.express == "j&t":
            shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
        elif co.express == "thailandpost":
            shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
        else:
            shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

        if co.payment == "cod":
            shipping_cost += 10

        co.shipping_cost = shipping_cost

    context["cart_order"] = cart_order

    return render(request, "firstapp/customer-all-order.html", context)

def UpdatePaid(request, order_id, status):
    try:
        if request.user.profile.usertype != 'admin':
            return redirect('home')
    except:
        return render(request, 'all-product')

    cart_order = CartOrder.objects.get(order_id=order_id)
    if status == "confirm":
        cart_order.paid = True
        cart_order.confirmed = True
        order_product = OrderProduct.objects.filter(order_id=order_id)

        for op in order_product:
            product = Product.objects.get(id=op.product_id)
            product.quantity = product.quantity - op.quantity
            product.save()

    return render(request, 'customer-all-product')

def CartOrderUpdateTracking(request, order_id):
    # try:
    #     if request.user.profile.usertype != 'admin':
    #         return redirect('home')
    # except:
    #     return render(request, 'all-product')

    if request.method == 'POST':
        cart_order = CartOrder.objects.get(order_id=order_id)
        data = request.POST.copy()

        tracking_number = data.get("tracking_number")
        cart_order.tracking_number = tracking_number
        cart_order.save()

        return redirect('customer-all-order')
    cart_order = CartOrder.objects.get(order_id=order_id)
    order_product = OrderProduct.objects.filter(order_id=order_id)

    total = sum([o.total for o in order_product])
    cart_order.total = total
    count = sum([o.quantity for o in order_product])

    if cart_order.express == "flash":
        shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
    elif cart_order.express == "kerry":
        shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
    elif cart_order.express == "j&t":
        shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
    elif cart_order.express == "thailandpost":
        shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

    if cart_order.payment == "cod":
        shipping_cost += 10

    cart_order.shipping_cost = shipping_cost

    context = {
        "cart_order": cart_order,
        "order_product": order_product,
        "total": total,
        "count": count
    }

    return render(request, "firstapp/cart-order-update-tracking.html", context)

def MyOrder(request, order_id):
    username = request.user.username
    user = User.objects.get(username=username)

    cart_order = CartOrder.objects.get(order_id=order_id)
    if user != cart_order.user:
        return redirect('all-product')

    order_product = OrderProduct.objects.filter(order_id=order_id)

    total = sum([o.total for o in order_product])
    cart_order.total = total
    count = sum([o.quantity for o in order_product])

    if cart_order.express == "flash":
        shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
    elif cart_order.express == "kerry":
        shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
    elif cart_order.express == "j&t":
        shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
    elif cart_order.express == "thailandpost":
        shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

    if cart_order.payment == "cod":
        shipping_cost += 10
    cart_order.shipping_cost = shipping_cost

    context = {"cart_order": cart_order, "order_product": order_product, "total":total, "count":count}

    return render(request, "firstapp/my-order.html", context)