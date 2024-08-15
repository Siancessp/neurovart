from django.contrib import admin
from .models import Customers, Payments, Wallet_transactions, Payouts,ApplyForFund, InvestmentForFund
# Register your models here.

admin.site.register(Customers)
admin.site.register(Payments)
admin.site.register(Wallet_transactions)
admin.site.register(Payouts)
admin.site.register(ApplyForFund)
admin.site.register(InvestmentForFund)