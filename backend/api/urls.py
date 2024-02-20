from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


from . import views
from . import endpoint

urlpatterns = [
    path('', views.index),
    path('get_user', views.get_user),
    path('contact', views.contactlist),
    path('newcontact', views.newcontactlist),
    path('message', views.message),
    path('status', views.status),
    path('user_status', views.user_status),
   
    #login,reg,logout
    path('register/', endpoint.register_user),
    path('verify_otp/', endpoint.otp_verification),

    #CRUD
    path('create', views.createmessage),
    path('createpost', views.createpost),
    

    #offline_online
    path('offline', views.offline),
    path('online', views.online),
    path('last_login', views.last_login),

    path('update_userbio', views.update_userbio),
    #User CRUD
    path('update_username', views.update_username),
    path('update_profile-pic', views.update_profilepic)
]

from .views import MyTokenObtainPairView
urlpatterns += [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]