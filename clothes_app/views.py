from django.shortcuts import render, redirect,HttpResponse
from .models import *
import logging
import random
from datetime import datetime
from .forms import *
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404

# Create your views here.

# Search part in index page
def indexSearch(request):
    # getting values
    search_type = request.GET.get('search_type')
    entry = request.GET.get('search_query')

    search_output = []

    # setting our type for search
    if search_type == 'priceSelect':
        if entry != '':
            search_output = Products.objects.filter(price__contains=entry)
    elif search_type == 'titleSelect':
        if entry != '':
            search_output = Products.objects.filter(title__contains=entry)

    # returning the result
    return search_output


# checking login
def checkLogin(request):
    if request.session.get('login'):
        return request.session.get('login').split('//')[0]
    else:
        return ''


# total price
def totalPrice(cart_all_items):
    total = 0
    for item in cart_all_items:
        total = total + (item.product.price * item.count)
    return total


# total count in cart
def totalCount(cart_all_items):
    total = 0
    for item in cart_all_items:
        total = total + item.count
    return total


# --------------------------------------------------------------------------------------------------------------------
# Create your views here.

'''----------------------------------------------------------------------------------------------------------------index---------------------------------'''


def index(request):
    # if user doesnt signed in
    error = ''

    # login
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = Client.objects.filter(phone=phone, password=password)

        if user:
            request.session['login'] = user[0].name + "//" + phone
            return redirect("/")
        else:
            error = 'شما ثبت نام نکرده اید ! برای این کار روی گزینه ی ثبت نام کلیک کنید'

    # main
    men = Products.objects.filter(category__category="لباس مردانه")
    women = Products.objects.filter(category__category="لباس زنانه")
    kids = Products.objects.filter(category__category="لباس بچگانه")
    accessory = Products.objects.filter(category__category="اکسسوری")

    # user login or not
    return render(request, "clothes_app/index.html", context={
        "men": men, "women": women, "kids": kids, "accessory": accessory, "error": error
        , "loginPart": checkLogin(request)}
                  )


'''----------------------------------------------------------------------------------------------------------------search---------------------------------'''


def search(request):
    context = []
    # search part
    if request.method == "GET":
        context = indexSearch(request)
    return render(request, "clothes_app/search.html", context={"data": context, "loginPart": checkLogin(request)})


'''----------------------------------------------------------------------------------------------------------------contact---------------------------------'''


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            person = form.cleaned_data['person']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            comment = Comment(person=person, email=email, text=text)
            comment.save()
    else:
        form = ContactForm()

    comments = Comment.objects.filter(show=True)
    return render(request, "clothes_app/contact.html",
                  context={"form": form, "comment": comments, "loginPart": checkLogin(request)})


'''----------------------------------------------------------------------------------------------------------------sign in---------------------------------'''


def signIn(request):
    # errors
    error = []

    # here we check that if user is logined , redirect it to index page
    if request.session.get('login'):
        return redirect("/")

    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        phone = request.POST['phone']

        # checking password
        if password == password_confirm:
            # checking length of password
            if len(password) > 7:

                # check that user doesnt exist to database
                user = Client.objects.filter(phone=phone)

                if user:
                    error.append("این کاربر قبلا ثبت نام کرده است!")
                else:
                    # creating user
                    Client.objects.create(name=username, phone=phone, password=password)
                    # creating session
                    request.session['login'] = username + "//" + phone
                    # redirecting
                    return redirect('/')
            else:
                error.append("رمز عبور باید بیشتر از 8 کارکتر باشد.")
        else:
            error.append("رمز عبور با تکرار آن یکسان نیست.")
    return render(request, "clothes_app/signIn.html", context={"error": error})


'''----------------------------------------------------------------------------------------------------------------log in---------------------------------'''


def logIn(request):
    # if user doesnt signed in
    error = ''

    # here we check that if user is logined , redirect it to index page
    if request.session.get('login'):
        return redirect("/")

    # check if user login or not
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = Client.objects.filter(phone=phone, password=password)
        if user:
            request.session['login'] = user[0].name + "//" + phone
            return redirect('/')
        else:
            error = 'شما ثبت نام نکرده اید ! برای این کار روی گزینه ی ثبت نام کلیک کنید'
    return render(request, "clothes_app/logIn.html", context={"error": error})


'''----------------------------------------------------------------------------------------------------------------log out-------------------------------'''


def logOut(request):
    # deleting session
    del request.session['login']
    return redirect("/")


'''---------------------------------------------------------------------------------------------------------------products-------------------------------'''


def products(request):
    # getting data from database and shuffle it
    products = list(Products.objects.all())
    random.shuffle(products)
    product = products

    return render(request, "clothes_app/products.html", context={"product": product, "loginPart": checkLogin(request)})


'''-----------------------------------------------------------------------------------------------------------single-products----------------------------'''


def single_product(request, product):
    theProduct = Products.objects.get(title=product)

    if request.method == 'GET':
        
        # here we check that if user is logined , redirect it to index page
        if request.session.get('login') is None:
            return redirect("/signIn/")
        
        count = request.GET.get('quantity')
        if count is not None:

            if checkLogin(request) != '':
                name = checkLogin(request)
                phone = request.session.get('login').split('//')[1]
                user = Client.objects.get(name=name, phone=phone)

                existProduct = Cart.objects.filter(client=user, product=theProduct)

                if existProduct.exists():
                    existProduct = existProduct[0]
                    existProduct.count = existProduct.count + int(count)
                    existProduct.save()
                else:
                    Cart.objects.create(client=user, product=theProduct, count=count)

                return redirect("/single-product/{}/".format(product))

    return render(request, "clothes_app/single-product.html",
                  context={"product": theProduct, "loginPart": checkLogin(request)})


'''---------------------------------------------------------------------------------------------------------------about us---------------------------------'''


def about(request):
    return render(request, "clothes_app/about.html", context={"loginPart": checkLogin(request)})


'''-----------------------------------------------------------------------------------------------------------------cart-----------------------------------'''


def cart(request):
    # here we check that if user is logined , redirect it to index page
    if request.session.get('login') is None:
        return redirect("/")

    name = checkLogin(request)
    phone = request.session.get('login').split('//')[1]
    user = Client.objects.get(name=name, phone=phone)

    # if we have get method it means that we have to add or remove from our products
    if request.method == "GET":

        productID = request.GET.get('productID')
        if productID is not None:
            productID = request.GET.get('productID').split('-')[0]
            productID = productID[1:]

            product = Products.objects.get(id=productID)

            cart_item = Cart.objects.filter(client=user, product=product).first()
            print(cart_item)
            action = request.GET.get('action')

            if action == "plus":
                cart_item.count = cart_item.count + 1
            elif action == 'minus':
                if cart_item.count > 1:
                    cart_item.count = cart_item.count - 1
            cart_item.save()

            return redirect('/cart/')

    cart_all_items = Cart.objects.filter(client=user)

    return render(request, "clothes_app/cart.html",
                  context={"loginPart": checkLogin(request),
                           "cart": cart_all_items,
                           "totalPrice": totalPrice(cart_all_items),
                           "totalCount": totalCount(cart_all_items)
                           })


'''----------------------------------------------------------------------------------------------------------delete from cart------------------------------'''


def deleteCart(request, productID):
    # here we check that if user is login , redirect it to index page
    if request.session.get('login') is None:
        return redirect("/")
    name = checkLogin(request)
    phone = request.session.get('login').split('//')[1]
    user = Client.objects.get(name=name, phone=phone)
    productInfo = Products.objects.get(id=productID)
    cart = Cart.objects.filter(client=user, product=productInfo)
    cart.delete()
    return redirect('/cart/')


'''-----------------------------------------------------------------------------------------------------------------invoice---------------------------------'''


def invoiceItem(request):
    # here we check that if user is logined , redirect it to index page
    if request.session.get('login') is None:
        return redirect("/")
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        invoice = Invoice.objects.get(id = item_id)
        invoice_item = InvoiceItem.objects.filter(invoice = invoice)
    
        return render(request , "clothes_app/invoiceItem.html",context={"loginPart": checkLogin(request),"invoice":invoice_item})


'''-----------------------------------------------------------------------------------------------------------------user-----------------------------------'''


def userPage(request):
    # here we check that if user is logined , redirect it to index page
    if request.session.get('login') is None:
        return redirect("/")

    # getting user data from database
    name = checkLogin(request)
    phone = request.session.get('login').split('//')[1]
    user = Client.objects.get(name=name, phone=phone)

    # get invoice
    invoice = Invoice.objects.filter(client = user)

    return render(request, "clothes_app/user.html", context={"loginPart": name, "user": user, "invoice":invoice})


# ----------------------------------------------------------payment-------------------------------------------------
def go_to_gateway_view(request):

    # here we check that if user is logined , redirect it to index page
    if request.session.get('login') is None:
        return redirect("/")

    phone = request.session.get('login').split('//')[1]
    client = Client.objects.get(phone = phone)
    price = totalPrice(Cart.objects.filter(client = client))
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = "09391838025"  # اختیاری

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.ZARINPAL)
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url('/callback-gateway')
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()
        print(bank.redirect_gateway().url)
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:

        # now its time to delete all carts and add the orders to factor

        # getting clinet informations
        phone = request.session.get('login').split('//')[1]
        client = Client.objects.get(phone = phone)

        #client carts
        carts = Cart.objects.filter(client = client)
        total_count = totalCount(carts)
        total_price = totalPrice(carts)

        #adding to invoice
        current_datetime = datetime.now()
        invoice = Invoice.objects.create(date = current_datetime , client = client , total_price = total_price , total_amount = total_count)

        #adding to invoice item
        for item in carts:
            InvoiceItem.objects.create(invoice=invoice, product=item.product, quantity=item.count, price=item.product.price)
        
        # deleting cart
        carts.delete()
        
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return render(request , "clothes_app/payment.html",context={"text":"پرداخت با موفقیت انجام شد"})
        

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return render(request , "clothes_app/payment.html",context={"text":"پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."})
    
