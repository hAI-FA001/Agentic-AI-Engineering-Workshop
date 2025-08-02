import datetime

# Mock get_share_price function as required by the prompt
def get_share_price(symbol):
    """
    Mock function to get the current price of a share.
    In a real application, this would query a market data API.
    """
    prices = {
        "AAPL": 170.0,
        "TSLA": 180.0,
        "GOOGL": 150.0,
    }
    return prices.get(symbol, 0.0) # Returns 0.0 if the symbol is not found

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0.0
        self.initial_deposit = 0.0
        self.holdings = {}  # {symbol: quantity}
        self.transactions = [] # list of dictionaries: {'timestamp': ..., 'type': ..., 'symbol': ..., 'quantity': ..., 'price': ..., 'amount': ...}

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        self.balance += amount
        if self.initial_deposit == 0:
            self.initial_deposit = amount
        self.transactions.append({
            'timestamp': datetime.datetime.now(),
            'type': 'DEPOSIT',
            'amount': amount
        })
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print(f"Insufficient funds for withdrawal. Available: ${self.balance:.2f}, Requested: ${amount:.2f}")
            return False
        self.balance -= amount
        self.transactions.append({
            'timestamp': datetime.datetime.now(),
            'type': 'WITHDRAWAL',
            'amount': amount
        })
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        return True

    def buy_shares(self, symbol, quantity):
        if quantity <= 0:
            print("Quantity must be positive.")
            return False

        price = get_share_price(symbol)
        if price == 0.0:
            print(f"Error: Invalid stock symbol '{symbol}'.")
            return False

        cost = price * quantity

        if cost > self.balance:
            print(f"Insufficient funds to buy {quantity} of {symbol}. Cost: ${cost:.2f}, Available balance: ${self.balance:.2f}")
            return False

        self.balance -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({
            'timestamp': datetime.datetime.now(),
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'amount': cost
        })
        print(f"Bought {quantity} of {symbol} @ ${price:.2f} each. Total cost: ${cost:.2f}. New balance: ${self.balance:.2f}")
        return True

    def sell_shares(self, symbol, quantity):
        if quantity <= 0:
            print("Quantity must be positive.")
            return False

        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            print(f"Insufficient shares of {symbol} to sell. You have {self.holdings.get(symbol, 0)}.")
            return False

        price = get_share_price(symbol)
        if price == 0.0:
            print(f"Error: Invalid stock symbol '{symbol}'.")
            return False

        revenue = price * quantity

        self.balance += revenue
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]

        self.transactions.append({
            'timestamp': datetime.datetime.now(),
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'amount': revenue
        })
        print(f"Sold {quantity} of {symbol} @ ${price:.2f} each. Total revenue: ${revenue:.2f}. New balance: ${self.balance:.2f}")
        return True

    def get_portfolio_value(self):
        """Calculates the current market value of all held shares."""
        current_portfolio_value = 0.0
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            current_portfolio_value += price * quantity
        return current_portfolio_value

    def get_total_account_value(self):
        """Calculates the total account value (balance + portfolio value)."""
        return self.balance + self.get_portfolio_value()

    def get_profit_loss(self):
        """Calculates the overall profit or loss based on the initial deposit."""
        if self.initial_deposit == 0:
            return 0.0 # No deposits yet, so no P/L
        return self.get_total_account_value() - self.initial_deposit

    def get_holdings_details(self):
        """Returns detailed information about current share holdings."""
        details = {}
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            cost_basis_per_share = self.get_average_purchase_price(symbol) # Get average cost
            current_value = quantity * price
            
            cost_basis_value = 0.0
            if cost_basis_per_share is not None:
                cost_basis_value = cost_basis_per_share * quantity
            
            pnl = current_value - cost_basis_value
            
            details[symbol] = {
                'quantity': quantity,
                'current_price': price,
                'current_value': current_value,
                'average_cost_per_share': cost_basis_per_share if cost_basis_per_share is not None else 'N/A',
                'total_pnl': pnl
            }
        return details

    def get_average_purchase_price(self, symbol):
        """Calculates the average purchase price for a given stock symbol."""
        total_spent_on_symbol = 0.0
        total_shares_bought = 0
        for tx in self.transactions:
            if tx['type'] == 'BUY' and tx['symbol'] == symbol:
                total_spent_on_symbol += tx['amount']
                total_shares_bought += tx['quantity']
        
        if total_shares_bought == 0:
            return None # No buys recorded for this symbol
        return total_spent_on_symbol / total_shares_bought

    def get_transactions_history(self):
        """Returns a list of all recorded transactions."""
        return self.transactions

    def report_account_status(self):
        """Prints a summary of the account's current status."""
        print(f"--- Account Status for {self.account_id} ---")
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"Initial Deposit: ${self.initial_deposit:.2f}")
        
        total_account_value = self.get_total_account_value()
        overall_pnl = self.get_profit_loss()
        pnl_symbol = "+" if overall_pnl >= 0 else ""

        print(f"Total Account Value: ${total_account_value:.2f}")
        print(f"Overall Profit/Loss: {pnl_symbol}${overall_pnl:.2f}")
        
        print("\nHoldings:")
        holdings_details = self.get_holdings_details()
        if not holdings_details:
            print("  No holdings.")
        else:
            for symbol, data in holdings_details.items():
                pnl_symbol_hold = "+" if data['total_pnl'] >= 0 else ""
                avg_cost_display = f"${data['average_cost_per_share']:.2f}" if isinstance(data['average_cost_per_share'], (int, float)) else data['average_cost_per_share']
                print(f"  {symbol}: {data['quantity']} shares @ ${data['current_price']:.2f} (Value: ${data['current_value']:.2f})")
                print(f"     Average Cost Basis: {avg_cost_display}")
                print(f"     Total P/L for {symbol}: {pnl_symbol_hold}${data['total_pnl']:.2f}")
        print("--------------------------")