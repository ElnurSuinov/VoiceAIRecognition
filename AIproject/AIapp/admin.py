from django.contrib import admin
from .models import DialogueLog, BankAccount, Transaction


@admin.register(DialogueLog)
class DialogueLogAdmin(admin.ModelAdmin):
    list_display = ("user_text", "intent", "created_at")
    ordering = ("-created_at",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "balance")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "target_account", "created_at")
    ordering = ("-created_at",)