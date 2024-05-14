from django.db import models
from django.conf import settings

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

class Firm (models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,blank=True,on_delete=models.PROTECT,related_name='firm_created_by' ,verbose_name='Create by' )
    name =models.CharField(max_length=350,null=False, verbose_name= "name")
    address =models.CharField(max_length=350,verbose_name= "Address")
    email =models.CharField(max_length=350,verbose_name= "Email")
    phone =models.CharField(max_length=350,verbose_name= "Phone")
    logo =models.ImageField(upload_to='firm_logo/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
            return f"{self.name}"

    class meta:
        app_label = "Firms"
        db_table = "firms"
        verbose_name_plural ="firms"
class Agency(models.Model):
    '''
        agencies model class
    '''
    firm  = models.ForeignKey('Firm', blank=True,on_delete=models.PROTECT,related_name='firm_attachement' ,verbose_name='Firm' )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='agaency_created_by' ,verbose_name='Create by' )
    name =models.CharField(max_length=350,null=False, verbose_name= "name")
    email =models.CharField(max_length=350,default='-',null=True, verbose_name= "Email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address =models.CharField(max_length=350,blank=True,null=True,verbose_name= "Adress")
    phone =models.CharField(max_length=350,blank=True,null=True,verbose_name= "Phone")
    
    class Meta:        
        verbose_name = "Agency"
        verbose_name_plural = "Agencies"

    def __str__(self) :
        return f"{self.name}"
    
    
       


class LiasonAgency(models.Model):
    ''' 
        this class allows the configuration of relationships between origin and destination agencies
    '''
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='liason_created_by' ,verbose_name='Created by' )
    origin = models.ForeignKey('Agency', blank=True,on_delete=models.PROTECT,related_name='origin' ,verbose_name='Origin agency' )
    destination = models.ForeignKey('Agency', blank=True,on_delete=models.PROTECT,related_name='destination' ,verbose_name='Destination agency' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.origin.name} => {self.destination.name}"
    
    class Meta:        
        verbose_name_plural ="Agencies liaison"

class InterrestRateConfig (models.Model):
    '''
        this class makes it possible to determine the interest rate per inter-agency transaction
    '''
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='rated_by' ,verbose_name='Config by' )
    agency_liason = models.ForeignKey('LiasonAgency', blank=True,on_delete=models.PROTECT,related_name='agency_relation' ,verbose_name='Agency relation' )   
    rate = models.FloatField(default= 0.00,verbose_name= "rate | Taux d'interêt")
    forfait = models.FloatField(default =0.00,verbose_name ="Forfait")
    threshold = models.FloatField(default =0.00,verbose_name ="threshold | seuil")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.agency_liason} : rate {self.rate} : forfait {self.forfait}"
    
    class Meta:
        
        verbose_name_plural ="Interest configurations"


    
