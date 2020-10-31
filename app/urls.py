
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('home/',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('forgetpassword/',views.forgetpassword,name="forgetpassword"),
    path('buy/',views.buy,name="buy"),
    path('buybooks/',views.buybooks,name="buybooks"),
    path('buycalculator/',views.buycalculator,name="buycalculator"),
    path('buydrafter/',views.buydrafters,name="buydrafter"),
    path('sell/',views.sell,name="sell"),
    path('addtocart/',views.addtocart,name="addtocart"),
    path('cart/',views.cart,name="cart"),
    path('main/',views.main,name="main"),
    path('main/',views.main,name="main"),
    path('successfull/',views.successfull,name='successfull')
]
