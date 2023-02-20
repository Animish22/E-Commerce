from distutils.command.upload import upload
from email.policy import default
from itertools import product
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    # Not our primary key as we have not set it as out primary key using primary key = true . therefore django itself creates a primary key  which cann be accessed by the name id in objects
    product_id  = models.AutoField
    # Default is not necessary to keep
    product_name = models.CharField(max_length = 50)
    category_name = models.CharField(max_length  = 100 , default = "")
    sub_category_name =  models.CharField(max_length = 100 , default="")
    price  = models.IntegerField(default =  0)
    emi_price = models.IntegerField(default = 0)
    desc = models.CharField(max_length = 300)
    pub_date = models.DateField()
    images = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key= True)
    items_json  = models.CharField(max_length=500 ,default="")
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default= 0)
    email = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    phone = models.CharField(max_length=70, default="")
    

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key= True)
    order_id =  models.IntegerField(default="")
    update_desc = models.CharField(max_length=500 ,default="")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self) :
        return self.update_desc[0:7] + "..."

class Review(models.Model):
    sno = models.AutoField(primary_key= True)
    comment = models.TextField(default="")
    user  = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    parent = models.ForeignKey('self' , on_delete=models.CASCADE , null=True)
    timestamp = models.DateTimeField(default = now)

    def __str__(self):
        return  self.comment[0:13] + "... by" +  self.user.username 



