from django.shortcuts import render,redirect
from .models import Category,Colours,NewLetterModel,SaleCollection,NewArrivals,Blog,CartItems,Product,DeliveryOption,PaxiPackages,CustomerModel
from django.contrib import messages
from django.db.models import Sum , F
from django.db.models import Q
import random

# Authentication Imports start 
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user
from django.contrib.auth.models import Group
# Authentication Imports end 


# Authentication Views start 

@unauthenticated_user
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userPath = request.POST.get('redictPath')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            current_user = request.user
            formCompletion = CustomerModel.objects.get(user = current_user)
            formCheck = formCompletion.formComplete
            if formCheck == "No":
                return redirect('client')
            elif userPath:
                return redirect(userPath)
            else:
                return redirect('index')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    return render(request, "Authentication/login.html")

# Agent Register view start 
@unauthenticated_user
def CustomerRegister(request):
    form = CreateUserForm()
    if request.method == 'POST' and 'create-customer' in request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            cleitnemail = form.cleaned_data.get('email')
            group = Group.objects.get(name= 'Customer')
            user.groups.add(group)
            CustomerModel.objects.create(
                user= user,
                first_name=username,
                email = cleitnemail
            )
            messages.success(request,'Account was created for ' + username)
            return redirect("login")

    context = {
        'form' : form
    }
    return render(request, "Authentication/customer_register.html", context)
# Agent Register View end 

# Employee Register View start 

# @unauthenticated_user
# def EmployeeRegister(request):
#     form = CreateUserForm()
#     if request.method == 'POST' and 'create-employee' in request.POST:
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             Employee.objects.create(
#                 user= user,
#                 first_name=username,
#             )
#             messages.success(request,'Account was created for ' + username)
#             return redirect("login")

#     context = {
#         'form' : form
#     }
#     return render(request, "Authentication/register.html", context)


# Employee Register view end 

def LogoutUser(request):
    logout(request)
    return redirect('login')
# Authentication Views end


# Customer Form Completion 
def CustomerForm(request):
    if request.method == 'POST' and 'complete_Registration' in request.POST:
        current_user = request.user
        updateCustomerForm = CustomerModel.objects.get(user = current_user)
        updateCustomerForm.first_name = request.POST.get('FirstName')
        updateCustomerForm.last_name = request.POST.get('LastName')
        updateCustomerForm.phone = request.POST.get('Phone')
        updateCustomerForm.formComplete = "Complete"
        updateCustomerForm.save()
        messages.success(request,'successfully Registed')
        userPath = request.POST.get('redictPath')
        if userPath:
            return redirect(userPath)
        else:
            return redirect('index')

    return render(request,'client/customerForm.html')




# Create your views here.
def IndexView(request):
    Categories = Category.objects.all()
    productOne_sale = Product.objects.filter(sale_CoverImages = "First")
    productTwo_sale = Product.objects.filter(sale_CoverImages = "second")
    productthird_sale = Product.objects.filter(sale_CoverImages = "third")
    BlogData = Blog.objects.all()
    # New Arrivals 
    arrivalOne = Product.objects.filter(Q(new = 'Yes') & Q(arrivals_CoverImages = 'First'))
    arrivalTwo = Product.objects.filter(Q(new = 'Yes') & Q(arrivals_CoverImages = 'second'))
    arrivalThree = Product.objects.filter(Q(new = 'Yes') & Q(arrivals_CoverImages = 'third'))

    if request.method == 'POST' and 'subcribe' in request.POST:
        subcribeUser = NewLetterModel()
        subcribeUser.first_name = request.POST.get('fistname')
        subcribeUser.last_name = request.POST.get('lastName')
        subcribeUser.email = request.POST.get('emailAddress')
        subcribeUser.save()
        messages.success(request,'successfully subscribed')


    # count cart 
    # Customer Instance 
    if request.user.is_authenticated:
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "Categories" : Categories,
        "productOne_sale" : productOne_sale,
        "productTwo_sale" : productTwo_sale,
        "productthird_sale" : productthird_sale,
        "arrivalOne" : arrivalOne,
        "arrivalTwo" : arrivalTwo,
        "arrivalThree" : arrivalThree,
        "BlogData" : BlogData,
        "cartCount" : cartCount
        }

        return render(request,'client/index.html',context)
  


    

    context = {
        "Categories" : Categories,
        "productOne_sale" : productOne_sale,
        "productTwo_sale" : productTwo_sale,
        "productthird_sale" : productthird_sale,
        "arrivalOne" : arrivalOne,
        "arrivalTwo" : arrivalTwo,
        "arrivalThree" : arrivalThree,
        "BlogData" : BlogData,
    }

    return render(request,'client/index.html',context)

def SaleCollectionS(request):
    sale_products = Product.objects.filter(sale = "Yes").order_by('-date_created')

    # cart Count 
    if request.user.is_authenticated:
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "sale_products" : sale_products,
        "cartCount" : cartCount
        }
        return render(request,'client/saleCollection.html',context)

    context = {
        "sale_products" : sale_products,
    }
    return render(request,'client/saleCollection.html',context)

def ItemDetails(request,item_id):
    item = Product.objects.get(id = item_id)
    ItemSizes = item.Sizes.all()


    if request.method == 'POST' and 'addCart' in request.POST:
        # Get Product Key 
        product_id = request.POST.get('ProductId')
        product = Product.objects.get(id = product_id)

        addCart = CartItems()
        # Customer Instance 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        addCart.CustomerId = customerInstance
        addCart.ProductKey = product
        addCart.Size = request.POST.get('sizeOptions')
        addCart.Quantity = request.POST.get('QuantityInput')
        addCart.Sub_Total =  request.POST.get('UnitTotal')
        addCart.sale_price = request.POST.get('product_price')  
        addCart.save()
        messages.success(request,'successfully added to cart')
        

    
    if request.user.is_authenticated:
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        customerCartCheck = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance))

        # Get Customer Cart count 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        if customerCartCheck:
            for i in customerCartCheck:
                if i.ProductKey.id == item_id:
                    inCartData = CartItems.objects.get( Q(satus = "cart") & Q(CustomerId = customerInstance) & Q(ProductKey = item_id))

                    context = {
                        "item": item,
                        "ItemSizes" : ItemSizes,
                        "inCartData" : inCartData,
                        "cartCount" : cartCount
                    }

                    return render(request,'client/itemDetails.html',context)
                    
    if request.user.is_authenticated:
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart count 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "item": item,
        "ItemSizes" : ItemSizes,
        "cartCount" : cartCount
        }

        return render(request,'client/itemDetails.html',context)

    context = {
        "item": item,
        "ItemSizes" : ItemSizes,
    }

    return render(request,'client/itemDetails.html',context)

def CartItemCollection(request):
    # Customer Instance 
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)
    # Get Customer Cart 
    ItemsData = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).order_by('-date_created')
    GrandTotal = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).values('Sub_Total')

    

    total = 0
    for order in GrandTotal:
        total = total + order['Sub_Total']

    # Remove Cart Item 
    if request.method == 'POST' and 'removeItem' in request.POST:
        product_id = request.POST.get('ItemID')
        cart = CartItems.objects.get(id = product_id)
        cart.delete()
        messages.success(request,'successfully removed')
        totalUpdate = request.POST.get('UpdateTotal')
        total = float(total) - float(totalUpdate)


    # subtract Quantity Function  
    if request.method == 'POST' and 'subtractQuantity' in request.POST:
        itemId = request.POST.get('productId')
        subtractQty = CartItems.objects.get(id = itemId)
        subtractQty.Quantity = int(subtractQty.Quantity) - 1
        priceCheck = subtractQty.sale_price
        subtractQty.Sub_Total = float(subtractQty.Sub_Total) - float(priceCheck)
        subtractQty.save()
        messages.success(request,'successfully updated')
        total = float(total) - float(priceCheck)

        if subtractQty.Quantity == 0:
            subtractQty.delete()

    # add Quantity Function  
    if request.method == 'POST' and 'addQuantity' in request.POST:
        itemId = request.POST.get('productId')
        subtractQty = CartItems.objects.get(id = itemId)
        subtractQty.Quantity = int(subtractQty.Quantity) + 1
        priceCheck = subtractQty.sale_price
        subtractQty.Sub_Total = float(subtractQty.Sub_Total) + float(priceCheck)
        subtractQty.save()
        messages.success(request,'successfully updated')
        total = float(total) + float(priceCheck)

    # Procced to checkout 
    if request.method == 'POST' and 'checkout' in request.POST:
        ItemsData = CartItems.objects.filter(Q(satus = "cart") & Q(CustomerId = customerInstance))


        saveDelivery = DeliveryOption()
        saveDelivery.CustomerId = customerInstance
        saveDelivery.GrandTotal = total
        saveDelivery.object_Name = "Pending Cart"
        saveDelivery.save()
        productId = saveDelivery.pk
        messages.success(request,'Almost Done!')
        saveDelivery.UserItems.add(*ItemsData)
        return redirect('delivery',productId)

    if request.user.is_authenticated:
        # cart Count 
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "ItemsData" : ItemsData,
        "total" : total,
        "cartCount" : cartCount
        }
        return render(request,'client/cart_items.html',context)


    context = {
        "ItemsData" : ItemsData,
        "total" : total,
    }
    return render(request,'client/cart_items.html',context)

def Checkout(request):
    return render(request,'client/checkout.html')

def Collection(request):
    Categories = Category.objects.all().order_by('date_created')

    # cart Count 
    if request.user.is_authenticated:
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "Categories" : Categories,
        "cartCount" : cartCount
        }
        return render(request,'client/collection.html',context)

    context = {
        "Categories" : Categories
    }
    return render(request,'client/collection.html',context)

def DeliveryOptions(request,item_id):
    # cart Count 
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)
    # Get Customer Cart 
    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

    # InStore Pick Up 
    if request.method == 'POST' and 'SubmitPickup' in request.POST:
        productUpdate = DeliveryOption.objects.get(id=item_id)
        productUpdate.Option_Picked = "Store"
        productUpdate.AmountDue = float(productUpdate.GrandTotal) 
        productUpdate.save()
        return redirect('payment',productUpdate.id)

    # Paxi Update Cart 
    if request.method == 'POST' and 'PaxiSubmit' in request.POST:
        productUpdate = DeliveryOption.objects.get(id=item_id)
        productUpdate.Option_Picked = "Paxi"
        productUpdate.save()
        return redirect('paxi',productUpdate.id)

    context = {
        "cartCount" : cartCount
    }

    return render(request,'client/delivery.html' ,context)

def PaxiDelivery(request,item_id):
    paxiOptions = PaxiPackages.objects.filter(Bag = "STANDARD BAG")

    # cart Count 
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)
    # Get Customer Cart 
    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

    if request.method == 'POST' and 'ConfirmLocation' in request.POST:
        updateItems = DeliveryOption.objects.get(id = item_id)
        packageId = request.POST.get('packageSelectedId')
        deliveryFee = PaxiPackages.objects.get(id = packageId)
        updateItems.paxiPackageId = packageId
        updateItems.deliveryFee = deliveryFee.price
        updateItems.addressLine1 = request.POST.get('address1')
        updateItems.addressLine2 = request.POST.get('address2')
        updateItems.addressLine3 = request.POST.get('address3')
        updateItems.addressLine4 = request.POST.get('address4')
        updateItems.addressLine5 = request.POST.get('address5')
        updateItems.addressLine6 = request.POST.get('address6')
        updateItems.addressLine7 = request.POST.get('address7')

        # update Amount Due  
        updateItems.AmountDue = float(deliveryFee.price)  + float(updateItems.GrandTotal) 
        
        updateItems.save()
        return redirect('payment',updateItems.id)

    context = {
        "paxiOptions" : paxiOptions,
        "cartCount": cartCount
    }
    return render(request,'client/paxi.html',context)

def Payment(request,item_id):
    CustomerCart = DeliveryOption.objects.get(id =item_id)
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)

    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()


    

    # User Information 
    if request.method == 'POST' and 'CompleteApplication' in request.POST:
        UpdateCartData = DeliveryOption.objects.get(id =item_id)
        UpdateCartData.Name = request.POST.get('FirstName')
        UpdateCartData.LastName = request.POST.get('LastName')
        UpdateCartData.Contact = request.POST.get('Phone')
        UpdateCartData.AltContact = request.POST.get('altPhone')
        UpdateCartData.Email = request.POST.get('Email')
        random_refrance = random.randrange(0, 1000000)
        current_user = request.user
        customer_referance = eval(f"{current_user.id}{random_refrance}")
        UpdateCartData.customer_ref = customer_referance

        # Update Cart status to Pending 
        updateCartStatus = UpdateCartData.UserItems.all()
        for i in updateCartStatus:
            statusUpdate = CartItems.objects.get(id= i.id)
            statusUpdate.satus = "pending"
            statusUpdate.save()

        UpdateCartData.save()
        messages.success(request,'Order has been completed. Thank you very much. Your order details and payment are given below.')
        return redirect('order-complete',UpdateCartData.id)

    context = {
        "CustomerCart" : CustomerCart,
        "customerInstance" : customerInstance,
        "cartCount" : cartCount
    }

    return render(request,'client/payment.html',context)

def CompleteOrder(request,item_id):
    customerReference = DeliveryOption.objects.get(id = item_id)
    # packageID = customerReference.paxiPackageId
    # paxiPack = PaxiPackages.objects.get(id = packageID)
    # paxiCost = paxiPack.price
     # cart Count 
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)
    # Get Customer Cart 
    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

    context = {
        "customerReference" : customerReference,
        "cartCount" : cartCount
       
    }
    return render(request,'client/complete.html',context)

def CustomerProducts(request):
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)

     # cart Count 
    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

    myCollection = DeliveryOption.objects.filter(CustomerId = customerInstance).order_by('-date_created')

    context = {
        "myCollection" : myCollection,
        "cartCount": cartCount
    }

    return render(request,'client/customerProducts.html',context)


def OrderComplete(request,order_id):
    current_user = request.user
    customerInstance = CustomerModel.objects.get(user = current_user)
    customerOrder = DeliveryOption.objects.get( Q(CustomerId = customerInstance) & Q(id = order_id))

    # cart Count 
    cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

    if customerOrder.Option_Picked == "Paxi":
        paxiData = PaxiPackages.objects.get(id = customerOrder.paxiPackageId)

        context = {
            "customerOrder" : customerOrder,
            "paxiData" : paxiData,
            "cartCount": cartCount
        }

        return render(request,'client/orderComplete.html',context)

    context = {
        "customerOrder" : customerOrder,
        "cartCount" : cartCount
    }
    return render(request,'client/orderComplete.html',context)

def PepParcel(request):
    return render(request,'client/pepParcel.html')

def ProductsPage(request):
    collection = Product.objects.all().order_by('-date_created')

    if request.user.is_authenticated:
        # cart Count 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "collection" : collection,
        "cartCount" : cartCount
        }
        return render(request,'client/products.html',context)
        
    context = {
        "collection" : collection,
    }
    return render(request,'client/products.html',context)


def Arrivals(request):
    collection = Product.objects.filter(new = "Yes")

    if request.user.is_authenticated:
        # cart Count 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "collection" : collection,
        "cartCount" : cartCount
        }
        return render(request,'client/arrivals.html',context)

    context = {
        "collection" : collection,
    }
    return render(request,'client/arrivals.html',context)

def NewsFeed(request):
    BlogData = Blog.objects.all()

    if request.user.is_authenticated:
        # cart Count 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
        "BlogData" : BlogData,
        "cartCount" : cartCount
        }
        return render(request,'client/newsFeed.html',context)

    context = {
        "BlogData" : BlogData,
    }
    return render(request,'client/newsFeed.html',context)
    
def AboutUs(request):
    if request.user.is_authenticated:
        # cart Count 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
            "cartCount" : cartCount
        }

        return render(request,'client/about.html',context)

    return render(request,'client/about.html')

def ContactUs(request):
    if request.user.is_authenticated:
        # cart Count 
        current_user = request.user
        customerInstance = CustomerModel.objects.get(user = current_user)
        # Get Customer Cart 
        cartCount = CartItems.objects.filter( Q(satus = "cart") & Q(CustomerId = customerInstance)).count()

        context = {
            "cartCount" : cartCount
        }

        return render(request,'client/contact.html',context)

    return render(request,'client/contact.html')


def Secondary(request):
    return render(request,'client/secondary_page.html')