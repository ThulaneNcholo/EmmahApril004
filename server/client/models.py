from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomerModel(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE,unique=True)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    formComplete = models.CharField(max_length=100,null=True,blank=True,default = 'No')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name

class Category(models.Model):
    Name = models.CharField(max_length=300,null=True)
    Category_Image = models.ImageField(null=True, blank=True,upload_to='files/CategoryImages')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Name

class ItemSize(models.Model):
    Size = models.CharField(max_length=300,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Size

class Colours(models.Model):
    Name = models.CharField(max_length=300,null=True)
    Hex = models.CharField(max_length=300,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Name

class LayByOptions(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True,default = 'Yes')
    Monthsdata = models.IntegerField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    DISPLAY = (
        ("Yes", "Yes"),
        ("No", "No"),
    )

    SALE_DISPLAY = (
        ("First", "First"),
        ("second", "second"),
        ("third", "third"),
    )
    Name = models.CharField(max_length=300,null=True)
    Description = models.TextField(blank = True,null=True)
    Price = models.FloatField(null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    ReStock_Level = models.IntegerField(null=True,blank=True)
    Category = models.ManyToManyField(Category,related_name="product_Category",blank=True,default=None)
    Colors = models.ManyToManyField(Colours,related_name="product_Colors",blank=True,default=None)
    Sizes = models.ManyToManyField(ItemSize,related_name="product_Sizes",blank=True,default=None)
    layby = models.ManyToManyField(LayByOptions,related_name="layBy_options",blank=True,default=None)
    main_Image = models.ImageField(null=True, blank=True,upload_to='files/ProductImages')
    Image_One = models.ImageField(null=True, blank=True,upload_to='files/ProductImages')
    Image_Two = models.ImageField(null=True, blank=True,upload_to='files/ProductImages')
    Image_Three = models.ImageField(null=True, blank=True,upload_to='files/ProductImages')
    main_display = models.CharField(max_length=10,choices=DISPLAY,default = 'No',null=True, blank=True)
    # Sale feature 
    sale = models.CharField(max_length=10,choices=DISPLAY,default = 'No',null=True, blank=True)
    Sale_Price = models.FloatField(null=True,blank=True)
    End_date = models.DateField(auto_now_add=False,null=True,blank=True)
    sale_CoverImages = models.CharField(max_length=10,choices=SALE_DISPLAY,default = 'No',null=True,blank=True)
    # Sale feature 
    new = models.CharField(max_length=10,choices=DISPLAY,default = 'No',null=True, blank=True)
    arrivals_CoverImages = models.CharField(max_length=10,choices=SALE_DISPLAY,default = 'No',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    


    def __str__(self):
        return self.Name

class SaleCollection(models.Model):
    DISPLAY = (
        ("First", "First"),
        ("second", "second"),
        ("third", "third"),
    )
    Product = models.ForeignKey(Product, on_delete=models.CASCADE , blank=True, related_name="sale_collection", default=None)
    Sale_Price = models.FloatField(null=True,blank=True)
    End_date = models.DateField(auto_now_add=False,null=True,blank=True)
    main_display = models.CharField(max_length=10,choices=DISPLAY,default = 'No')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Product.Name

class NewArrivals(models.Model):
    DISPLAY = (
        ("First", "First"),
        ("second", "second"),
        ("third", "third"),
    )
    Product = models.ForeignKey(Product, on_delete=models.CASCADE , blank=True, related_name="new_arrivals", default=None)
    Sale_Price = models.FloatField(null=True,blank=True)
    End_date = models.DateField(auto_now_add=False,null=True,blank=True)
    main_display = models.CharField(max_length=10,choices=DISPLAY,default = 'No')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Product.Name

class Blog(models.Model):
    Title = models.CharField(max_length=300,null=True,blank=True)
    Sub_heading = models.CharField(max_length=300,null=True,blank=True)
    Description = models.TextField(blank = True,null=True)
    Blog_Image = models.ImageField(null=True, blank=True,upload_to='files/BlogImages')
    Street = models.CharField(max_length=300,null=True,blank=True)
    Suburb = models.CharField(max_length=300,null=True,blank=True)
    City_Town = models.CharField(max_length=300,null=True,blank=True)
    Province = models.CharField(max_length=300,null=True,blank=True)
    Event_TimeStart = models.CharField(max_length=300,null=True,blank=True)
    Event_TimeEnd = models.CharField(max_length=300,null=True,blank=True)
    Event_Startdate = models.DateField(auto_now_add=False,null=True,blank=True)
    Event_EndDate = models.DateField(auto_now_add=False,null=True,blank=True)
    LinkOne = models.CharField(max_length=1000,null=True,blank=True)
    LinkTwo = models.CharField(max_length=1000,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.Title

class CartItems(models.Model):
    ITEMSTATUS = (
        ("cart", "cart"),
        ("pending", "pending"),
        ("paid", "paid"),
        ("complete", "complete"),
    )
    CustomerId = models.ForeignKey(CustomerModel, blank=True, null=True,on_delete=models.CASCADE,related_name="customer_cart",default=None)
    ProductKey = models.ForeignKey(Product, on_delete=models.CASCADE , blank=True, related_name="cart_key", default=None)
    Size = models.CharField(max_length=300,null=True,blank=True)
    Quantity = models.IntegerField(null=True,blank=True)
    Sub_Total = models.FloatField(null=True,blank=True)
    sale_price = models.FloatField(null=True,blank=True)
    satus = models.CharField(max_length=100,choices=ITEMSTATUS,default = 'cart')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.ProductKey.Name

class PaxiPackages(models.Model):
    Bag = models.CharField(max_length=300,null=True,blank=True)
    size = models.CharField(max_length=300,null=True,blank=True)
    days = models.CharField(max_length=50,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.days

class DeliveryOption(models.Model):
    CustomerId = models.ForeignKey(CustomerModel, blank=True, null=True,on_delete=models.CASCADE,related_name="customer_order",default=None)
    UserItems = models.ManyToManyField(CartItems,related_name="user_cart",blank=True,default=None)
    Option_Picked = models.CharField(max_length=100,null=True,blank=True)
    GrandTotal = models.FloatField(null=True,blank=True)
    AmountDue = models.FloatField(null=True,blank=True)
    Name = models.CharField(max_length=300,null=True,blank=True)
    LastName = models.CharField(max_length=300,null=True,blank=True)
    Contact = models.CharField(max_length=300,null=True,blank=True)
    AltContact = models.CharField(max_length=300,null=True,blank=True)
    Email = models.CharField(max_length=300,null=True,blank=True)
    ComplexDetails = models.CharField(max_length=300,null=True,blank=True)
    Street = models.CharField(max_length=300,null=True,blank=True)
    Suburb = models.CharField(max_length=300,null=True,blank=True)
    City = models.CharField(max_length=300,null=True,blank=True)
    Province = models.CharField(max_length=300,null=True,blank=True)
    PostalCode = models.CharField(max_length=300,null=True,blank=True)
    object_Name = models.CharField(max_length=300,null=True,blank=True)
    customer_ref = models.CharField(max_length=100,null=True,blank=True,unique=True)
    # paxi data 
    paxiPackageId = models.CharField(max_length=100,null=True,blank=True)
    deliveryFee = models.FloatField(null=True,blank=True)
    addressLine1 = models.CharField(max_length=300,null=True,blank=True)
    addressLine2 = models.CharField(max_length=300,null=True,blank=True)
    addressLine3 = models.CharField(max_length=300,null=True,blank=True)
    addressLine4 = models.CharField(max_length=300,null=True,blank=True)
    addressLine5 = models.CharField(max_length=300,null=True,blank=True)
    addressLine6 = models.CharField(max_length=300,null=True,blank=True)
    addressLine7 = models.CharField(max_length=300,null=True,blank=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.object_Name

class NewLetterModel(models.Model):
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=200,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name
