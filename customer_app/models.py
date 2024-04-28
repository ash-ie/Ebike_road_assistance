from django.db import models

from accounts.models import BaseModel, User

# Create your models here.
class Request(BaseModel):
    cat=(('two wheeler with gear','two wheeler with gear'),('two wheeler without gear','two wheeler without gear'))
    category=models.CharField(max_length=50,choices=cat)
    vehicle_no=models.PositiveIntegerField(null=False)
    vehicle_name = models.CharField(max_length=40,null=False)
    vehicle_model = models.CharField(max_length=40,null=False)
    vehicle_brand = models.CharField(max_length=40,null=False)
    problem_description = models.CharField(max_length=500,null=False)
    date=models.DateField(auto_now=True)
    cost=models.PositiveIntegerField(null=True)
    customer=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='customer_request')
    mechanic=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    stat=(('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status=models.CharField(max_length=50,choices=stat,default='Pending',null=True)
    bill_status = models.IntegerField(default=0,null=True)
    location = models.CharField(max_length=50,null=True)

class Feedback(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    message=models.TextField(null=True,blank=True)

class CreditCard(BaseModel):
    card_no = models.CharField(max_length=30,null=True,blank=True)
    card_cvv = models.CharField(max_length=30,null=True,blank=True)
    expiry_date = models.CharField(max_length=100,null=True,blank=True)