Thought: The user wants a Python module named `accounts.py` that implements an `Account` class for a trading simulation. I need to define the `Account` class with methods for creating an account, depositing/withdrawing funds, buying/selling shares, calculating portfolio value, P/L, reporting holdings, P/L, transactions, and handling invalid operations. I also need to include a test implementation for `get_share_price`.

Here's a breakdown of the steps:
1.  **Define `get_share_price` function**: Create a mock function for `get_share_price` as specified.
2.  **Create `Account` class**:
    *   **`__init__`**: Initialize account with `balance`, `initial_deposit`, `holdings` (a dictionary of {symbol: quantity}), and `transactions` (a list of transaction details).
    *   **`deposit(amount)`**: Add funds to the balance. Update `initial_deposit` if it's the first deposit.
    *   **`withdraw(amount)`**: Subtract funds from the balance, ensuring the balance doesn't go negative.
    *   **`buy_shares(symbol, quantity)`**:
        *   Get current share price using `get_share_price`.
        *   Calculate the cost.
        *   Check if sufficient balance.
        *   If affordable, deduct cost from balance, add/update holdings, and record the transaction.
    *   **`sell_shares(symbol, quantity)`**:
        *   Get current share price.
        *   Calculate the revenue.
        *   Check if the user owns enough shares.
        *   If valid, add revenue to balance, update/remove holdings, and record the transaction.
    *   **`get_portfolio_value()`**: Calculate the total value of all held shares based on current market prices. Add this to the current balance to get the total account value.
    *   **`get_profit_loss()`**: Calculate P/L based on the difference between the current total account value and the `initial_deposit`.
    *   **`get_holdings()`**: Return the `holdings` dictionary.
    *   **`get_transactions()`**: Return the `transactions` list.
    *   **`get_pnl_details()`**: A helper to get P/L for each holding and overall.
3.  **Structure the output**: Ensure the final output is just the Python code for `accounts.py`.

Let's start by defining the `get_share_price` function and then the `Account` class. I will use `datetime` for transaction timestamps.

**`get_share_price` implementation:**
```python
def get_share_price(symbol):
    prices = {
        "AAPL": 170.0,
        "TSLA": 180.0,
        "GOOGL": 150.0,
    }
    return prices.get(symbol, 0.0) # Return 0 if symbol not found
```

**`Account` class implementation:**
```python
import datetime

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
        print(f"Deposited {amount:.2f}. New balance: {self.balance:.2f}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print("Insufficient funds for withdrawal.")
            return False
        self.balance -= amount
        self.transactions.append({
            'timestamp': datetime.datetime.now(),
            'type': 'WITHDRAWAL',
            'amount': amount
        })
        print(f"Withdrew {amount:.2f}. New balance: {self.balance:.2f}")
        return True

    def buy_shares(self, symbol, quantity):
        if quantity <= 0:
            print("Quantity must be positive.")
            return False

        price = get_share_price(symbol)
        if price == 0.0:
            print(f"Invalid stock symbol: {symbol}")
            return False

        cost = price * quantity

        if cost > self.balance:
            print(f"Insufficient funds to buy {quantity} of {symbol}. Cost: {cost:.2f}, Available balance: {self.balance:.2f}")
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
        print(f"Bought {quantity} of {symbol} at {price:.2f} each. Total cost: {cost:.2f}. New balance: {self.balance:.2f}")
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
            print(f"Invalid stock symbol: {symbol}")
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
        print(f"Sold {quantity} of {symbol} at {price:.2f} each. Total revenue: {revenue:.2f}. New balance: {self.balance:.2f}")
        return True

    def get_portfolio_value(self):
        current_portfolio_value = 0.0
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            current_portfolio_value += price * quantity
        return current_portfolio_value

    def get_total_account_value(self):
        return self.balance + self.get_portfolio_value()

    def get_profit_loss(self):
        if self.initial_deposit == 0:
            return 0.0 # No deposits yet, so no P/L
        return self.get_total_account_value() - self.initial_deposit

    def get_holdings_details(self):
        details = {}
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            details[symbol] = {
                'quantity': quantity,
                'current_price': price,
                'current_value': quantity * price
            }
        return details

    def get_profit_loss_per_holding(self):
        pnl_per_holding = {}
        for symbol, data in self.get_holdings_details().items():
            # To calculate P/L per holding accurately, we need to track the average buy price.
            # For this simplified version, we'll just show current value and assume cost basis is complex.
            # A more robust system would store purchase cost basis per transaction.
            # For now, we report current value and assume P/L calculation is overall.
            # If we MUST show P/L per holding, we'd need to change transaction structure.
            # Let's stick to overall P/L as per requirements.
            pass # Placeholder, as overall P/L is requested.
        return "Detailed P/L per holding is not supported in this simplified version. Use get_profit_loss() for overall."

    def get_transactions_history(self):
        return self.transactions

    def report_account_status(self):
        print(f"--- Account Status for {self.account_id} ---")
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"Initial Deposit: ${self.initial_deposit:.2f}")
        print(f"Total Account Value: ${self.get_total_account_value():.2f}")
        overall_pnl = self.get_profit_loss()
        pnl_symbol = "+" if overall_pnl >= 0 else ""
        print(f"Overall Profit/Loss: {pnl_symbol}${overall_pnl:.2f}")
        print("Holdings:")
        if not self.holdings:
            print("  No holdings.")
        else:
            for symbol, data in self.get_holdings_details().items():
                pnl_value = data['current_value'] - (self.get_cost_basis(symbol) if self.get_cost_basis(symbol) is not None else data['current_value']) # Simplified cost basis assumption
                pnl_symbol_hold = "+" if pnl_value >= 0 else ""
                print(f"  {symbol}: {data['quantity']} shares @ ${data['current_price']:.2f} (Value: ${data['current_value']:.2f}) P/L: {pnl_symbol_hold}${pnl_value:.2f}")
        print("--------------------------")

    def get_cost_basis(self, symbol):
        # This is a simplified way to estimate cost basis.
        # A real system would need to track cost basis per buy transaction (e.g., FIFO, LIFO, Average Cost).
        # For this example, we'll assume we can find *some* transaction for the symbol.
        # This is a very crude approximation and might not be accurate if multiple buys/sells occurred.
        total_spent_on_symbol = 0
        total_shares_bought = 0
        for tx in self.transactions:
            if tx['type'] == 'BUY' and tx['symbol'] == symbol:
                total_spent_on_symbol += tx['amount']
                total_shares_bought += tx['quantity']
        if total_shares_bought == 0:
            return None # No buys for this symbol
        return total_spent_on_symbol / total_shares_bought * self.holdings.get(symbol, 0)


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

```
The prompt asks for the output to be *ONLY* the raw Python code. I need to combine the `get_share_price` function and the `Account` class into a single script and then print only that code. I should also remove print statements from methods that are not explicitly for reporting, and use return values instead where appropriate for programmatic use, but the prompt implies interactive use with print statements for feedback. I'll keep the print statements for user feedback as that aligns with a "simple account management system" interaction.

Let's refine `get_profit_loss_per_holding` to actually try and calculate it, even if simplified.
The `get_cost_basis` needs to be improved to handle the actual purchase cost more accurately if we want P/L per holding.
Let's track average purchase price.
When buying, update average price:
`new_avg_price = ((old_avg_price * old_quantity) + (cost_of_new_buy)) / (old_quantity + new_quantity)`
When selling, we need to know *which* shares were sold. FIFO (First-In, First-Out) is common.
This requires storing purchases as a list of (price, quantity) tuples per symbol.

For simplicity and to meet the prompt's implicit complexity level, let's stick to overall P/L and report holdings value. The `get_cost_basis` can be a placeholder or just use the total spent divided by total shares, which is average cost basis, and assume that's what's used for P/L calculation per holding.

Let's refine `get_holdings_details` and `report_account_status` to show P/L per holding based on a simplified average cost basis.

My `get_cost_basis` function calculates the average price paid per share *for all shares of that symbol ever bought*, then multiplies by the *current* quantity held. This is a reasonable simplification for "average cost basis" without implementing FIFO/LIFO.

For `report_account_status`, I need to calculate P/L per holding.
`pnl_value = data['current_value'] - (average_cost_per_share * data['quantity'])`
Where `average_cost_per_share` is derived from transactions.

The `get_cost_basis` method is already defined and calculates the average cost of all shares ever purchased for a symbol. I will use this.

Let's ensure all print statements are informative.
The prompt requests "ONLY the raw Python code without any markdown formatting, code block delimiters or backticks."

The code should be self-contained in `accounts.py`.

Final check on requirements:
-   Create account: `Account(account_id)` in `__init__`.
-   Deposit funds: `deposit()`.
-   Withdraw funds: `withdraw()`.
-   Buy/Sell shares: `buy_shares()`, `sell_shares()`.
-   Calculate total portfolio value: `get_portfolio_value()` (shares value) and `get_total_account_value()` (balance + shares value).
-   Profit or loss from initial deposit: `get_profit_loss()`.
-   Report holdings: `get_holdings_details()` and `report_account_status()`.
-   Report profit or loss: `get_profit_loss()` and `report_account_status()`.
-   List transactions: `get_transactions_history()`.
-   Prevent negative balance/unaffordable buys/selling non-existent shares: Handled in `withdraw`, `buy_shares`, `sell_shares`.
-   `get_share_price` mock: Included.

I will put all code into one block and ensure no extra prints or markdown.
```python
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
            cost_basis_value = cost_basis_per_share * quantity if cost_basis_per_share is not None else 0 # If no cost basis, assume 0 for PNL calculation
            pnl = current_value - cost_basis_value
            details[symbol] = {
                'quantity': quantity,
                'current_price': price,
                'current_value': current_value,
                'average_cost_per_share': cost_basis_per_share if cost_basis_per_share is not None else 'N/A',
                'pnl_per_share': pnl / quantity if quantity > 0 and cost_basis_per_share is not None else 'N/A',
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

```
The prompt specifies that I should ONLY output raw python code. No markdown. No extra text.
I have to make sure the final output contains *only* the python code.
My thought process has led me to the complete code. Now I just need to ensure it's presented correctly.
The prompt implies that the `get_share_price` function should be accessible within the module, and the `Account` class should use it.

The code looks good. It covers all requirements. The `report_account_status` provides a good summary, including P/L per holding.
The prompt is very specific about "ONLY the raw Python code without any markdown formatting, code block delimiters or backticks". I will present only the python code.import datetime

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