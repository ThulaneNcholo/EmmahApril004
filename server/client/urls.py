from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
     # Authentication urls start 
    path('login/', views.LoginPage,name="login"),
    path('register/', views.CustomerRegister,name="register"),
    path('logout/', views.LogoutUser,name="logout"),
    # path('employee/', views.EmployeeRegister,name="employee"),
    # Authentication urls end 

    # password reset urls start  
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="Authentication/password_reset.html"
    ), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="Authentication/password_reset_sent.html"
    ), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="Authentication/password_reset_form.html"
    ),name="password_reset_confirm"),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="Authentication/password_reset_done.html"
    ), name="password_reset_complete"),
    # password reset urls end 


    path('client/',views.CustomerForm,name='client'),

    path('',views.IndexView,name='index'),
    path('secondaryPage/',views.Secondary,name='secondaryPage'),
    path('on-sale/',views.SaleCollectionS,name='on-sale'),
    path('item-details/<int:item_id>',views.ItemDetails,name='item-details'),
    path('cart/',views.CartItemCollection,name='cart'),
    path('checkout/',views.Checkout,name='checkout'),
    path('collection/',views.Collection,name='collection'),
    path('delivery/<int:item_id>',views.DeliveryOptions,name='delivery'),
    path('payment/<int:item_id>',views.Payment,name='payment'),
    path('paxi/<int:item_id>',views.PaxiDelivery,name='paxi'),
    path('pep-parcel/',views.PepParcel,name='pep-parcel'),
    path('all-collections/',views.ProductsPage,name='all-collections'),
    path('new-arrival/',views.Arrivals,name='new-arrival'),
    path('news-feed/',views.NewsFeed,name='news-feed'),
    path('about-us/',views.AboutUs,name='about-us'),
    path('contact/',views.ContactUs,name='contact'),
    path('complete/<int:item_id>',views.CompleteOrder,name='complete'),


    # New Complete Order url 
    path('order-complete/<int:order_id>',views.OrderComplete,name='order-complete'),

    # customer Products 
    path('my-collection/',views.CustomerProducts,name='my-collection'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

