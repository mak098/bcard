from django.db import models
from django.conf import settings
from Agency.models import InterrestRateConfig,Agency
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

class CashIn(models.Model):

    code = models.CharField(max_length=350,null=False, verbose_name= "Code")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='transaction_created_by' ,verbose_name='Created by' )
    interrest_config = models.ForeignKey(InterrestRateConfig, blank=True,on_delete=models.PROTECT,related_name='interrest_rate' ,verbose_name='Destination' )
    amount = models.FloatField(default= 0.00,verbose_name= "Amount")
    sender = models.CharField(max_length=350,null=False, verbose_name= "Sender")
    sender_phone = models.CharField(max_length=50,null=False, verbose_name= "Sender phone")
    recipient = models.CharField(max_length=350,null=False, verbose_name= "Recipient")
    recipient_phone = models.CharField(max_length=350,null=False, verbose_name= "Recipient phone")
    comment = models.TextField(max_length=200,null=True, blank=True,verbose_name= "Comment")
    interrest = models.JSONField(default={"type":""})
    status = models.BooleanField(default=False, verbose_name ="is served")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.code}"
    
    class Meta:      
        verbose_name_plural = "cash In"
    
class CashOut(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null =True,blank=True,on_delete=models.PROTECT,related_name='transaction_cashout_by' ,verbose_name='Created by' )
    cash_in = models.ForeignKey(CashIn, blank=True,on_delete=models.PROTECT,related_name='transaction_cashout' ,verbose_name='Transaction' )
    amount = models.FloatField(default= 0.00,verbose_name= "Amount")
    recipient = models.CharField(max_length=350,null = True, verbose_name= "Recipient")
    recipient_phone = models.CharField(max_length=350,null = True, verbose_name= "Recipient phone")
    comment = models.TextField(max_length=200,null=True,blank=True, verbose_name= "Comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.transaction.code}"
    
    class Meta:        
        verbose_name_plural ="Cash out"

class Interrest (models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null =True,blank=True,on_delete=models.PROTECT,related_name='transaction_interrest' ,verbose_name='Created by' )
    cash_in = models.ForeignKey(CashIn, blank=True,on_delete=models.PROTECT,related_name='transaction_interrest' ,verbose_name='Transaction' )
    amount = models.FloatField(default= 0.00,verbose_name= "Amount")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:        
        verbose_name_plural ="Interests"

    
# @receiver(post_save, sender=CashIn)   
# def generate_transaction_code(sender, instance, **kwargs):
#     import datetime
#     today = datetime.date.today()
#     year = today.year
#     user_id = instance.created_by.id
#     origin_agence =instance.created_by.agency_id
    
    
#     CashIn.objects.filter(id=instance.id).update(
#         code = f"{user_id}.{origin_agence}.{instance.id}.{year}"
#     )
    # transaction.save()

    



