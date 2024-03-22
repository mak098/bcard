from django.db import models
from django.conf import settings
from Agency.models import Firm

class Wallet (models.Model):
    owner = models.ForeignKey(Firm, null=True, blank=True,
		on_delete=models.PROTECT, related_name='firm_owner')
    amount = models.FloatField(default=0, verbose_name="amount")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Wallets'
        
    def __str__(self):
        return f"{self.owner.name} amount: {self.amount} $"

class Transaction(models.Model):

	
    wallet = models.ForeignKey(Wallet, null=False,on_delete=models.PROTECT, related_name='owner_wallet')
    reason = models.CharField(max_length=200,  default='recharge', blank=True)
    amount = models.FloatField(default=0, blank=True)
    operation = models.CharField(max_length=20, blank=True,  default='get',
		choices=(
			('get', 'get'),
			('out', 'out')			
		),
        verbose_name='Operation',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Transactions'

    def __str__(self):
	    return self.reason
    
    