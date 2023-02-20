# File made by ME 
from django.shortcuts import render , redirect , HttpResponse
from .models import Product , Contact , Order , OrderUpdate , Review
from math import ceil
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.utils.timezone import now

# Create your views here.

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]


    allProds = []
    catprods = Product.objects.values('category_name' ,'id')
    # print(catprods) -> all the categories for each object
    # print(type(catprods)) -> quesryset
    cats = set()
    # cats should be a set coz a set doesn't allow duplicate values in it
    for item in catprods:
        # print(item) -> {'category' -> 'category value'}
        # print(type(item)) -> dictionary
        cats.add(item['category_name'])
    # print(cats) -> set with unique categories
    # print(type(cats)) -> set

    for cat in cats:
        prod = Product.objects.filter(category_name=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([
            prod, range(1, nSlides), nSlides
        ])

    params = {
        'allProds' : allProds
    }
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        
        if len(name) <  2 or len(email) < 4 or len(phone)  <10 or len(desc) < 5:
            messages.error(request , "Please enter correct credentials.")
        else:
            messages.success(request , "Your feedback has been submitted:")
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
    return render(request, "shop/contact.html")


def searchMatch(query , item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category_name.lower() or query in item.product_name or query in item.category_name or query in item.desc:
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allProds =[]
    catprods = Product.objects.values('category_name' , 'id')
    cats = set()
    for item in catprods :
        cats.add(item['category_name'])
    
    for cat in cats:
        prodtemp = Product.objects.filter(category_name = cat)
        prod = [item for item in prodtemp if searchMatch(query , item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        thank = False
        if len(prod) != 0 :
                print(len(prod))
                allProds.append([prod , range(1,nSlides) , nSlides])
    if len(allProds) == 0 :
        thank = True
    return render(request, 'shop/search.html',{'allProds' : allProds , 'thank' : thank})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('items_json', '')
        amount = request.POST.get('amount' ,'')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2' , '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')
        if len(name) < 2 or len(email) < 10 or len(phone) < 10 :
            messages.error(request , "Please enter correct credentials")
        else:
            thank = True
            order = Order(items_json = items_json ,amount = amount , name=name, email=email,address = address , city = city, state = state,zip_code =zip_code , phone = phone)
            order.save()
            id = order.order_id
            update = OrderUpdate(order_id = order.order_id  , update_desc = "Your order has been placed . ")
            update.save()
            return render(request, 'shop/checkout.html',{'thank' : thank , 'id' : id})
    return render(request, 'shop/checkout.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates , order[0].items_json], default=str)
                return HttpResponse(response)
            else: 
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def handleSignup(request):
    if request.method == "POST":
        Signupusername = request.POST.get("Signupusername")
        email = request.POST.get("email")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pass1 =  request.POST.get("pass1")
        pass2 =  request.POST.get("pass2")
        if len(Signupusername) > 10 :
            messages.error(request, "Plase Enter User name within the limit ")
            return redirect('/shop/')
        if pass1 != pass2 :
            messages.error(request ,"Passwords do not match")
            return redirect('/shop/')
        user = User.objects.create_user(Signupusername , email , pass1)
        user.first_name = fname
        user.last_name  = lname
        user.save()
        return redirect('/shop/')
    else:
        return HttpResponse("404 - Not found ")

def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password")
        user = authenticate(username = username , password = password)

        if user is not None:
            login(request , user)
            messages.success(request, "You were logged in successfully")
            return redirect('/shop/')
        else:
            messages.error(request , "Please Enter valid username and password")
            return redirect('/shop/')

def handleLogout(request):
    logout(request)
    messages.success(request , "You were logged in successfully")
    return redirect('/shop/')

def productView(request,myid):
    product = Product.objects.filter(id = myid)
    related_prod = Product.objects.filter(category_name = product[0].category_name)
    # print(related_prod)
    reviews = Review.objects.filter(product = product[0])
    n = len(related_prod)
    nSlides = n//4 + ceil((n/4) - (n//4))
    return render(request, 'shop/productView.html',{'product' : product[0] ,'related_prod' :  related_prod , 'nSlides':nSlides ,'range':range(1,nSlides) , 'reviews' : reviews}) 
    #instead of making a variable parameters we directly pased the parameters.
    # the thing in quotes is the name with which the vriable product will be sent to the productView page

def PostReview(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        productSno = request.POST.get("productSno")
        product = Product.objects.get(id = productSno)
        review = Review(comment = comment , user = user ,product = product)
        review.save()
        messages.success(request, "Message was submitted successfully.")
    return redirect(f"/shop/productview/{product.id}")


