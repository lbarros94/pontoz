from decimal import Decimal


class MonthlyReport:
    def __init__(self, month, year, sale,pointz_sale,base_coin_cost):
        self.base_coin_cost = Decimal(base_coin_cost)
        self.pointz_sale = Decimal(pointz_sale)
        self.sale = Decimal(sale)
        self.year = year
        self.month = month

    @property
    def header(self):
        return f'{self.month}-{self.year}'
