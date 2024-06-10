from django.urls import path
from . import views


urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    path('', views.loginPage, name='login'),
    path('signup/',views.signup,name='signup'),
    # path('password_reset', views.password_reset_request, name="password_reset")
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('forgetpassword/<str:id>',views.create_password,name='create_password'),
    # path('changepassword/',views.changepassword,name='changepassword'),
    # path('Fporegistation/',views.Fporegistation,name='Fporegistation'),
    path('userverify/<str:id>',views.userverify,name='userverify'),
    path('autologin/<str:id>',views.autologin,name='autologin'),
    path('numberverify/',views.numberverify,name='numberverify'),
    path('otpverify/',views.otpverify,name='otpverify'),
    path('logout/',views.logout_view,name='logout'),
    path('home/',views.home,name='home'),
    path('createcustomer/',views.createcustomer,name='createcustomer'),
    path('customerview/<int:id>',views.customerview,name='customerview'),

]
