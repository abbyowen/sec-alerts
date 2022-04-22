class Ticker:

    # Instance variables that will hold various features of the shoe
    def __init__(self, filing_date, trade_date, ticker, company, industry, ins, trade_type, price, qty, owned, delta_own, value):
        self.filing_date = filing_date
        self.trade_date = trade_date
        self.ticker = ticker
        self.company = company
        self.industry = industry
        self.ins = ins
        self.trade_type = trade_type
        self.price = price
        self.qty = qty
        self.owned = owned
        self.delta_own = delta_own
        self.value = value

    # Function for comparing two objects by their shoe IDs
    def __eq__(self, obj):
        if self.filing_date == obj.filing_date:
            return True
        else:
            return False

    def txt_row(self):
        return self.filing_date + "," + self.ticker + "," + self.company + "," + self.industry + "," + self.trade_type + "," + self.price + "," + self.qty + "," + self.owned + "," + self.delta_own + "," + self.value
    
    # String representation of the shoe
    def __str__(self):
        return "Filing Date: " + self.filing_date + "\n" + "Ticker: " + self.ticker + "\n" + "Company: " + self.company + "\n" + "Industry: " + self.industry + "\n" + "Trade Type: " + self.trade_type + "\n" + "Price: " + self.price + "\n" + "Quantity: " + self.qty + "\n" + "Owned: " + self.owned + "\n" + "ΔOwn: " + self.delta_own + "\n" + "Value: " + self.value
