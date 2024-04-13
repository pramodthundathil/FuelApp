from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm, FuelAddForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .decorators import admin_only, unautenticated_user
from .models import StaffProfile, FuelStocks, FuelRequest, FuelPrice
from django.db.models import Sum
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")

@unautenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        # fname = request.POST["fname"]
        # email = request.POST["email"]
        # uname = request.POST["uname"]
        # pswd = request.POST["pswd"]
        # pswd1 = request.POST["pswd1"]

        # if pswd != pswd1:
        #     messages.info(request,"Password Do not Matches..")
        #     return redirect("SignUp")
        # if User.objects.filter(username = uname).exists():
        #     messages.info(request,"Username alredy exists user another username")
        #     return redirect("SignUp")
        # if User.objects.filter(email = email).exists():
        #     messages.info(request,"Email alredy exists user another email")
        #     return redirect("SignUp")

        form = UserAddForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")
        
    return render(request,"register.html",{"form":form})


@login_required(login_url="SignIn")
def AddStaff(request):
    form = UserAddForm()
    if request.method == "POST":
       
        form = UserAddForm(request.POST)
        phone = request.POST["phonenumber"]
        address = request.POST["address"]

        if form.is_valid():
            user = form.save()
            user.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group)

            StaffProfile.objects.create(phone = phone, address = address, user = user).save()
            messages.success(request,"Staff Created.. Please Login....")
            return redirect("Mystaff")
        
    return render(request,"addstaff.html",{"form":form})


def SignOut(request):
    logout(request)
    return redirect('SignIn')




@admin_only
def Index(request):
    price = FuelPrice.objects.get(id = 1)
    context = {
        "price":price
    }
    return render(request,"index.html",context)


def AdminIndex(request):
    fuel_petrol = FuelStocks.objects.filter(fuel_category = "Petrol").aggregate(total_value=Sum('stock'))['total_value'] or 0
    fuel_diesel = FuelStocks.objects.filter(fuel_category = "Diesel").aggregate(total_value=Sum('stock'))['total_value'] or 0
    fuel_LPG = FuelStocks.objects.filter(fuel_category = "LPG").aggregate(total_value=Sum('stock'))['total_value'] or 0
    # print(fuel_petrol,"-------------------------")

    context = {
        "fuel_petrol":fuel_petrol,
        "fuel_diesel":fuel_diesel,
        "fuel_LPG":fuel_LPG
    }
    return render(request,"adminindex.html",context)


def Mystaff(request):
    staff = User.objects.filter(groups__name = "staff")

    context = {
        "staff":staff
    }
    return render(request,"mystaff.html",context)

def Deletestaff(request,pk):
    User.objects.get(id = pk).delete()
    messages.success(request,"Staff deleted.........")
    return redirect(Mystaff)


def Fuelstock(request):
    stock = FuelStocks.objects.filter(user = request.user)


    context = {
        "stock":stock
    }
    return render(request,"fuelstock.html",context)


def AddFuelstock(request):
    form = FuelAddForm()
    if request.method == "POST":
        form = FuelAddForm(request.POST)
        if form.is_valid():
            stock = form.save()
            stock.user = request.user
            stock.save()
            messages.success(request,"Stock Addedd........")
            return redirect("Fuelstock")

    context = {
        "form":form
    }
    return render(request,"addfuelstock.html",context)


def UpdateStock(request,pk):
    fuel = FuelStocks.objects.get(id = pk)
    if request.method == "POST":
        stock = request.POST['stock']
        fuel.stock += float(stock)
        fuel.save()
        messages.success(request,"Stock Updated........")
        return redirect("Fuelstock")
    
    return redirect("Fuelstock")

def deleteStock(request,pk):
    FuelStocks.objects.get(id = pk).delete()
    messages.success(request,"Stock deleted........")
    return redirect("Fuelstock")



# requests fuels and updates ........................................

def FuelRequests(request):
    if request.method == "POST":
        fuel = request.POST['type']
        qunty = request.POST['qunty']
        name = request.POST['name']
        location = request.POST['location']
        try:
            lat = request.POST['lat']
            log = request.POST['log']
        except:
            lat = 9.9185
            log = 76.2558
        phone = request.POST['phonenumber']

        fuel_request = FuelRequest.objects.create(user = request.user,fuel = fuel,qunty = qunty, name = name,location = location, phone = phone, latitude = lat,logitude = log,delivery_status = "Fuel Ordered"  )
        fuel_request.save()

        stock = FuelStocks.objects.filter(fuel_category = fuel).first()
        stock.stock -= float(qunty)
        stock.save()

        mail_subject = 'Fuel Order Confirmed'
        message = render_to_string('emailbody.html', {'name': name,
                                                      "address":location,
                                                        "fuel":fuel,
                                                        "date":fuel_request.date_time,
                                                        "Quantity":qunty,
                                                        
                                                        })

        email = EmailMessage(mail_subject, message, to=[request.user.email])
        email.send(fail_silently=True)
        price = FuelPrice.objects.get(id = 1)
        if fuel == "Petrol":
            val = price.Petrol
        elif fuel == "Diesel":
            val = price.Diesel
        else:
            val = price.LPG
        currency = 'INR'
        amount = val  * 100 * float(qunty) # Rs. 200
        context = {}

    # Create a Razorpay Order Pyament Integration.....
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                            currency=currency,
                            payment_capture='0'))

    # order id of newly created order.
        razorpay_order_id = razorpay_order["id"]
        callback_url = "PurchaseHistory/"

    # we need to pass these details to frontend.
        
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context["total_pay"] = amount/100
        context['currency'] = currency
        context['callback_url'] = callback_url 
        context['slotid'] = "1",
        

        messages.info(request,"Fuel Order Confiremd........")
        return render(request,"makepayment.html",context)
    
    return render(request,"fuelrequests.html")


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')

@csrf_exempt
def PurchaseHistory(request):
    fuelrequest = FuelRequest.objects.filter(user = request.user)[::-1]

    context = {
        "fuelrequest":fuelrequest
    }
    return render(request,"purchasehistory.html",context)


def StaffIndex(request):
    fuel_petrol = FuelStocks.objects.filter(fuel_category = "Petrol").aggregate(total_value=Sum('stock'))['total_value'] or 0
    fuel_diesel = FuelStocks.objects.filter(fuel_category = "Diesel").aggregate(total_value=Sum('stock'))['total_value'] or 0
    fuel_LPG = FuelStocks.objects.filter(fuel_category = "LPG").aggregate(total_value=Sum('stock'))['total_value'] or 0
    # print(fuel_petrol,"-------------------------")

    context = {
        "fuel_petrol":fuel_petrol,
        "fuel_diesel":fuel_diesel,
        "fuel_LPG":fuel_LPG
    }
    return render(request,"staffindex.html",context)


def CustomerFuelRequest(request):
    fuelrequest = FuelRequest.objects.filter(completion_status = False)[::-1]

    context = {
        "fuelrequest":fuelrequest
    }

    return render(request,'customerfuelrequests.html',context)

def OrderTaken(request,pk):
    fuelorder = FuelRequest.objects.get(id = pk)
    fuelorder.status = True
    fuelorder.delivery_status = "Order Taken Deliver soon"
    fuelorder.staff = request.user
    fuelorder.save()
    messages.info(request,"Order status changed........")
    return redirect("CustomerFuelRequest")


def OrderDeliveryChange(request,pk):
    fuelorder = FuelRequest.objects.get(id = pk)
    fuelorder.delivery_status = "Order is on progress deliver soon...."
    fuelorder.save()
    messages.info(request,"Order status changed........")
    return redirect("CustomerFuelRequest")


def OrderDelivered(request,pk):
    fuelorder = FuelRequest.objects.get(id = pk)
    fuelorder.delivery_status = "Your Order Delivered"
    fuelorder.completion_status = True
    fuelorder.save()
    messages.info(request,"Order status changed........")
    return redirect("CustomerFuelRequest")

def DeliveryHistory(request):
    fuelrequest = FuelRequest.objects.filter(completion_status = True)[::-1]

    context = {
        "fuelrequest":fuelrequest
    }
    return render(request,"deliveryhistory.html",context)


def ViewInMap(request,pk):
    fuelorder = FuelRequest.objects.get(id = pk)
    lat = fuelorder.latitude
    log = fuelorder.logitude

    context = {
        "lat":float(lat),
        "log":float(log)
    }
    return render(request,"viewinmap.html",context)


def FuelPriceUpdate(request):
    price = FuelPrice.objects.get(id =1)
    if request.method == "POST":
        petrol = request.POST['petrol']
        diesel = request.POST['diesel']
        lpg = request.POST['lpg']

        price.Petrol = petrol
        price.Diesel = diesel
        price.LPG = lpg
        price.save()
        messages.info(request,"Order status changed........")
        return redirect("FuelPriceUpdate")
    
    context = {
        "price":price
    }
    return render(request,"fuelpriceupdate.html",context)

def AdminViewFuelRequests(request):

    fuelrequest = FuelRequest.objects.all()

    context = {
        "fuelrequest":fuelrequest
    }

    return render(request,"adminfuelreqests.html",context)


def DeleteOrderByCustomer(request,pk):
    FuelRequest.objects.get(id = pk).delete()
    messages.info(request,"Order Cancelled....")
    return redirect("PurchaseHistory")


