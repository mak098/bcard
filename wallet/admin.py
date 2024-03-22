from django.contrib import admin
from .models import Wallet,Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
