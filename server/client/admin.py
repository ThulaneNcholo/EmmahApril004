from django.contrib import admin
from .models import Category,Colours,ItemSize,Product,SaleCollection,NewArrivals,Blog,CartItems,DeliveryOption,LayByOptions,PaxiPackages,CustomerModel,NewLetterModel
# Register your models here.
class CatoegoryAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'date_created'
    )

class ItemSizeAdmin(admin.ModelAdmin):
    list_display = (
        'Size', 'date_created'
    )

class ColoursAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'Hex', 'date_created'
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'Name', 'Price', 'Quantity','ReStock_Level'
    )

class SaleCollectionAdmin(admin.ModelAdmin):
    list_display = (
        'Product','main_display', 'Sale_Price', 'End_date'
    )

class NewArrivalsAdmin(admin.ModelAdmin):
    list_display = (
        'Product', 'main_display',
    )

class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'Title', 'Event_Startdate','Event_EndDate'
    )

class CartsAdmin(admin.ModelAdmin):
    list_display = (
        'ProductKey', 'Size','Quantity','Sub_Total','sale_price','satus'
    )

class DeliveryOptionsAdmin(admin.ModelAdmin):
    list_display = (
        'object_Name','Option_Picked','Name','Contact'
    )

class LaybyOptionsAdmin(admin.ModelAdmin):
    list_display = (
        'name','Monthsdata',
    )

class PaxiPackageAdmin(admin.ModelAdmin):
    list_display = (
        'Bag','size','days','price'
    )

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'user','first_name','last_name','email','phone'
    )

class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'first_name','last_name','email'
    )

admin.site.register(Category,CatoegoryAdmin)
admin.site.register(ItemSize,ItemSizeAdmin)
admin.site.register(Colours,ColoursAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(SaleCollection,SaleCollectionAdmin)
admin.site.register(NewArrivals,NewArrivalsAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(CartItems,CartsAdmin)
admin.site.register(DeliveryOption,DeliveryOptionsAdmin)
admin.site.register(LayByOptions,LaybyOptionsAdmin)
admin.site.register(PaxiPackages,PaxiPackageAdmin)
admin.site.register(CustomerModel,CustomerAdmin)
admin.site.register(NewLetterModel,NewsletterAdmin)


