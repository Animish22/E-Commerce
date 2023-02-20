# Admin wala import on url kewal main site me hona chahiye and not in any of the apps 
from django.urls import path , include
from . import views

urlpatterns = [
    path('' ,views.index,name ="ShopHome"),
    path('about/' ,views.about,name ="About Shop"),
    path('contact/' ,views.contact,name ="Contact Us"),
    path('tracker/' ,views.tracker,name ="Track Order"),
    path('search/' ,views.search,name ="Search Product"),
    path('signup/', views.handleSignup , name="handleSignup"),
    path('login/', views.handleLogin , name="handleLogin"),
    path('logout/', views.handleLogout , name="handleLogout"),
    path('productview/<int:myid>' ,views.productView,name ="View Product"),
    path('checkout/' ,views.checkout,name ="Checkout"),   
    path('postreview/' ,views.PostReview,name ="PostReview"),   
]