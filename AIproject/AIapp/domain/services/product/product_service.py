from AIapp.models import DepositProduct,LoanProduct, CardProduct

class ProductService:
    def get_deposits(self):

        return DepositProduct.objects.all()

    def get_loans(self):

        return LoanProduct.objects.all()

    def get_cards(self):

        return CardProduct.objects.all()