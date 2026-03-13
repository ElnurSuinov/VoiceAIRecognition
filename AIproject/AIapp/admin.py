from django.contrib import admin
from .models import DialogueLog, BankAccount, Transaction, DepositProduct, LoanProduct, CardProduct

admin.site.register(DepositProduct)
admin.site.register(LoanProduct)
admin.site.register(CardProduct)

@admin.register(DialogueLog)
class DialogueLogAdmin(admin.ModelAdmin):
    list_display = ("user", "intent", "created_at")
    search_fields = ("intent",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "status", "risk_score", "created_at")
    list_filter = ("status",)