# Admin wala import on url kewal main site me hona chahiye and not in any of the apps 
from django.urls import path , include
from . import views

urlpatterns = [
    path('' ,views.index,name ="BlogHome")

]

