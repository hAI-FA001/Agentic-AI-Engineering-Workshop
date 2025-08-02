The user wants a Gradio UI in `app.py` to demonstrate the `Account` class from `accounts.py`. I need to create a Python script that imports the `Account` class and uses Gradio components to interact with its methods.

Here's a breakdown of the UI components and their corresponding `Account` methods:

1.  **Account Creation**:
    *   Input: `account_id` (Textbox)
    *   Action: Call `Account(account_id)` to create an account.
    *   Output: Success/Error message.
    *   Need a global variable to hold the single `Account` instance.

2.  **Deposit Funds**:
    *   Input: `amount` (Number)
    *   Action: Call `account.deposit(amount)`
    *   Output: Success/Error message, updated balance.

3.  **Withdraw Funds**:
    *   Input: `amount` (Number)
    *   Action: Call `account.withdraw(amount)`
    *   Output: Success/Error message, updated balance.

4.  **Buy Shares**:
    *   Input: `symbol` (Textbox), `quantity` (Number)
    *   Action: Call `account.buy_shares(symbol, quantity)`
    *   Output: Success/Error message, updated balance, updated holdings.

5.  **Sell Shares**:
    *   Input: `symbol` (Textbox), `quantity` (Number)
    *   Action: Call `account.sell_shares(symbol, quantity)`
    *   Output: Success/Error message, updated balance, updated holdings.

6.  **View Portfolio**:
    *   Action: Call `account.get_holdings()`, `account.get_balance()`, `account.get_portfolio_value()`, `account.get_total_account_value()`, `account.get_profit_loss()`.
    *   Output: Display holdings (Dataframe/JSON), current balance, portfolio value, total account value, P/L.

7.  **View Transactions**:
    *   Action: Call `account.get_transactions()`
    *   Output: Display transactions (Dataframe/JSON).

I will structure the Gradio app using `gr.Blocks` to create a more organized interface with tabs or sections for different operations.

Let's start building `app.py`:

*   Import `gradio` and `Account`, `Transaction` from `accounts`.
*   Initialize a global `account` variable to `None`.
*   Define helper functions that will be called by Gradio components. These functions will interact with the `account` object.
*   Create the Gradio interface using `gr.Blocks`.

**Detailed Plan for `app.py`:**

*   **Global Account**: `account = None`
*   **Account Creation Function**:
    *   Takes `account_id`.
    *   If `account` is `None`, create `Account(account_id)`.
    *   Update `account` global variable.
    *   Return success message.
    *   Handle cases where account already exists.
*   **Deposit Function**:
    *   Takes `amount`.
    *   Check if `account` exists.
    *   Call `account.deposit(amount)`.
    *   Return status message and updated balance.
*   **Withdraw Function**:
    *   Takes `amount`.
    *   Check if `account` exists.
    *   Call `account.withdraw(amount)`.
    *   Return status message and updated balance.
*   **Buy Shares Function**:
    *   Takes `symbol`, `quantity`.
    *   Check if `account` exists.
    *   Call `account.buy_shares(symbol, quantity)`.
    *   Return status message, updated balance, and updated holdings display.
*   **Sell Shares Function**:
    *   Takes `symbol`, `quantity`.
    *   Check if `account` exists.
    *   Call `account.sell_shares(symbol, quantity)`.
    *   Return status message, updated balance, and updated holdings display.
*   **Display Account Summary Function**:
    *   Check if `account` exists.
    *   Get balance, holdings, portfolio value, total value, P/L.
    *   Format holdings into a displayable string or list.
    *   Return these values.
*   **Display Transactions Function**:
    *   Check if `account` exists.
    *   Get transactions.
    *   Format transactions into a list of strings or a DataFrame.
    *   Return the formatted transactions.

**Gradio Interface Structure:**

```python
import gradio as gr
import accounts # Assuming accounts.py is in the same directory

# Global variable to hold the single account instance for this demo
account = None

def create_or_get_account(account_id_input):
    global account
    if not account_id_input:
        return "Error: Account ID cannot be empty.", None, None, None, None, None, None, None
    if account is None:
        try:
            account = accounts.Account(account_id_input)
            return f"Account '{account_id_input}' created successfully.", account_id_input, 0.0, {}, 0.0, 0.0, 0.0, []
        except ValueError as e:
            return f"Error creating account: {e}", None, None, None, None, None, None, None
    else:
        if account.account_id == account_id_input:
            return f"Account '{account_id_input}' already active.", account.account_id, account.balance, account.holdings, account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
        else:
            return f"Error: Another account ('{account.account_id}') is already active. Please restart the demo to switch accounts.", None, None, None, None, None, None, None

def deposit_funds(amount_input):
    if account is None:
        return "Error: No account active. Please create an account first.", None, None, None, None, None, None
    try:
        amount = float(amount_input)
        if account.deposit(amount):
            return f"Deposit successful. Amount: ${amount:.2f}", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
        else:
            # Error messages are printed by the Account class methods directly
            return f"Deposit failed.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    except (ValueError, TypeError):
        return "Error: Invalid amount entered for deposit.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()

def withdraw_funds(amount_input):
    if account is None:
        return "Error: No account active. Please create an account first.", None, None, None, None, None, None
    try:
        amount = float(amount_input)
        if account.withdraw(amount):
            return f"Withdrawal successful. Amount: ${amount:.2f}", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
        else:
            return f"Withdrawal failed.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    except (ValueError, TypeError):
        return "Error: Invalid amount entered for withdrawal.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()

def buy_shares(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active. Please create an account first.", None, None, None, None, None, None
    if not symbol_input:
        return "Error: Symbol cannot be empty.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    try:
        quantity = int(quantity_input)
        if account.buy_shares(symbol_input, quantity):
            return f"Bought {quantity} shares of {symbol_input}.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
        else:
            return f"Buy order failed for {symbol_input}.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    except (ValueError, TypeError):
        return "Error: Invalid quantity entered for buying shares.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()

def sell_shares(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active. Please create an account first.", None, None, None, None, None, None
    if not symbol_input:
        return "Error: Symbol cannot be empty.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    try:
        quantity = int(quantity_input)
        if account.sell_shares(symbol_input, quantity):
            return f"Sold {quantity} shares of {symbol_input}.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
        else:
            return f"Sell order failed for {symbol_input}.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()
    except (ValueError, TypeError):
        return "Error: Invalid quantity entered for selling shares.", account.balance, account.get_holdings(), account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), account.get_transactions()

def display_summary():
    if account is None:
        return "No account active.", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
    
    holdings_dict = account.get_holdings()
    holdings_str = "\n".join([f"{symbol}: {qty}" for symbol, qty in holdings_dict.items()]) if holdings_dict else "No holdings"
    
    balance = account.get_balance()
    portfolio_value = account.get_portfolio_value()
    total_value = account.get_total_account_value()
    profit_loss = account.get_profit_loss()
    initial_deposit = account.get_initial_deposit()

    return (f"Account ID: {account.account_id}",
            f"${balance:.2f}",
            holdings_str,
            f"${portfolio_value:.2f}",
            f"${total_value:.2f}",
            f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})",
            account.get_transactions()) # Return transactions to update the transactions table


# Gradio Interface Definition
with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulation")

    # --- Account Management Section ---
    with gr.Row():
        account_id_input = gr.Textbox(label="Account ID", placeholder="Enter your desired Account ID")
        create_account_btn = gr.Button("Create/Activate Account")

    account_status_output = gr.Textbox(label="Account Status", interactive=False)
    active_account_id_display = gr.Textbox(label="Active Account ID", interactive=False)
    current_balance_display = gr.Number(label="Current Balance", interactive=False)
    holdings_display = gr.Textbox(label="Current Holdings", interactive=False)
    portfolio_value_display = gr.Number(label="Portfolio Value", interactive=False)
    total_account_value_display = gr.Number(label="Total Account Value", interactive=False)
    profit_loss_display = gr.Textbox(label="Profit/Loss (vs Initial Deposit)", interactive=False)

    # --- Transaction Section ---
    with gr.Tabs():
        with gr.TabItem("Deposit/Withdraw"):
            with gr.Row():
                deposit_amount_input = gr.Number(label="Amount to Deposit")
                withdraw_amount_input = gr.Number(label="Amount to Withdraw")
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            deposit_status_output = gr.Textbox(label="Deposit Status", interactive=False)
            withdraw_status_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        with gr.TabItem("Buy/Sell Shares"):
            with gr.Row():
                share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
                share_quantity_input = gr.Number(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            buy_sell_status_output = gr.Textbox(label="Buy/Sell Status", interactive=False)

        with gr.TabItem("Account Summary & Transactions"):
            view_summary_btn = gr.Button("Refresh Account Summary")
            transactions_display = gr.DataFrame(
                headers=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Amount", "Description"],
                datatype=["str", "str", "str", "str", "str", "str", "str"],
                interactive=False,
                label="Transaction History"
            )

    # --- Event Listeners ---
    create_account_btn.click(
        fn=create_or_get_account,
        inputs=[account_id_input],
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    deposit_btn.click(
        fn=deposit_funds,
        inputs=[deposit_amount_input],
        outputs=[deposit_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    withdraw_btn.click(
        fn=withdraw_funds,
        inputs=[withdraw_amount_input],
        outputs=[withdraw_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    buy_btn.click(
        fn=buy_shares,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    sell_btn.click(
        fn=sell_shares,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    view_summary_btn.click(
        fn=display_summary,
        outputs=[account_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Refresh summary whenever any transaction happens
    # This might be too much, but for simplicity:
    deposit_btn.click(fn=display_summary, outputs=[account_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    withdraw_btn.click(fn=display_summary, outputs=[account_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    buy_btn.click(fn=display_summary, outputs=[account_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    sell_btn.click(fn=display_summary, outputs=[account_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])


demo.launch()
```

Refining the `display_summary` and how it updates the transaction table.
The `transactions_display` needs to be updated by a function that fetches transactions.
I will use `gr.DataFrame` for transactions.

The `create_or_get_account` function should also update all the summary fields and the transaction table when an account is activated.

```python
import gradio as gr
import accounts # Assuming accounts.py is in the same directory

# Global variable to hold the single account instance for this demo
account = None

def format_transactions_for_display(transactions):
    """Formats a list of Transaction objects into a list of lists for gr.DataFrame."""
    if not transactions:
        return []
    
    formatted_data = []
    for tx in transactions:
        formatted_data.append([
            tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            tx.transaction_type,
            tx.symbol if tx.symbol else "",
            tx.quantity if tx.quantity is not None else "",
            f"{tx.price:.2f}" if tx.price is not None else "",
            f"{tx.amount:.2f}",
            tx.description
        ])
    return formatted_data

def update_account_displays():
    """Helper function to return all current account state for display components."""
    if account is None:
        return "No account active.", None, 0.0, "", 0.0, 0.0, 0.0, []
    
    holdings_dict = account.get_holdings()
    holdings_str = "\n".join([f"{symbol}: {qty}" for symbol, qty in holdings_dict.items()]) if holdings_dict else "No holdings"
    
    balance = account.get_balance()
    portfolio_value = account.get_portfolio_value()
    total_value = account.get_total_account_value()
    profit_loss = account.get_profit_loss()
    initial_deposit = account.get_initial_deposit()

    return (f"Account ID: {account.account_id}",
            account.account_id,
            balance,
            holdings_str,
            portfolio_value,
            total_value,
            f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})",
            format_transactions_for_display(account.get_transactions()))

def create_or_get_account(account_id_input):
    global account
    if not account_id_input:
        return "Error: Account ID cannot be empty.", None, 0.0, "", 0.0, 0.0, 0.0, []
        
    if account is None:
        try:
            account = accounts.Account(account_id_input)
            return f"Account '{account_id_input}' created successfully.", account.account_id, account.balance, "No holdings", account.get_portfolio_value(), account.get_total_account_value(), account.get_profit_loss(), []
        except ValueError as e:
            return f"Error creating account: {e}", None, 0.0, "", 0.0, 0.0, 0.0, []
    else:
        if account.account_id == account_id_input:
            return f"Account '{account_id_input}' already active.", account.account_id, account.balance, "\n".join([f"{s}: {q}" for s, q in account.holdings.items()]) if account.holdings else "No holdings", account.get_portfolio_value(), account.get_total_account_value(), f"${account.get_profit_loss():.2f} (Initial Deposit: ${account.get_initial_deposit():.2f})", format_transactions_for_display(account.get_transactions())
        else:
            return f"Error: Another account ('{account.account_id}') is already active. Please restart the demo to switch accounts.", None, 0.0, "", 0.0, 0.0, 0.0, []

def process_transaction(transaction_func, *args):
    """Generic function to handle deposit, withdraw, buy, sell and update displays."""
    if account is None:
        return "Error: No account active. Please create an account first.", account.balance if account else 0.0, account.holdings if account else {}, account.get_portfolio_value() if account else 0.0, account.get_total_account_value() if account else 0.0, account.get_profit_loss() if account else 0.0, format_transactions_for_display(account.get_transactions() if account else [])

    status_msg = ""
    try:
        success = transaction_func(*args)
        if success:
            status_msg = "Transaction successful." # Specific message handled by transaction_func if needed
        else:
            status_msg = "Transaction failed. Check logs for details." # Account class prints specific errors
    except Exception as e:
        status_msg = f"An error occurred: {e}"
        
    return status_msg, *update_account_displays()[1:] # Return status and all updated account displays

def deposit_wrapper(amount_input):
    return process_transaction(account.deposit, float(amount_input))

def withdraw_wrapper(amount_input):
    return process_transaction(account.withdraw, float(amount_input))

def buy_shares_wrapper(symbol_input, quantity_input):
    if not symbol_input: return "Error: Symbol cannot be empty.", *update_account_displays()[1:]
    try:
        quantity = int(quantity_input)
        return process_transaction(account.buy_shares, symbol_input, quantity)
    except (ValueError, TypeError):
        return "Error: Invalid quantity entered.", *update_account_displays()[1:]

def sell_shares_wrapper(symbol_input, quantity_input):
    if not symbol_input: return "Error: Symbol cannot be empty.", *update_account_displays()[1:]
    try:
        quantity = int(quantity_input)
        return process_transaction(account.sell_shares, symbol_input, quantity)
    except (ValueError, TypeError):
        return "Error: Invalid quantity entered.", *update_account_displays()[1:]


with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulation")

    # --- Account Management Section ---
    with gr.Row():
        account_id_input = gr.Textbox(label="Account ID", placeholder="Enter your desired Account ID")
        create_account_btn = gr.Button("Create/Activate Account")

    account_status_output = gr.Textbox(label="Account Status", interactive=False)
    active_account_id_display = gr.Textbox(label="Active Account ID", interactive=False)
    current_balance_display = gr.Number(label="Current Balance", interactive=False)
    holdings_display = gr.Textbox(label="Current Holdings", interactive=False, lines=3)
    portfolio_value_display = gr.Number(label="Portfolio Value", interactive=False)
    total_account_value_display = gr.Number(label="Total Account Value", interactive=False)
    profit_loss_display = gr.Textbox(label="Profit/Loss (vs Initial Deposit)", interactive=False)

    # --- Transaction Section ---
    with gr.Tabs():
        with gr.TabItem("Deposit/Withdraw"):
            with gr.Row():
                deposit_amount_input = gr.Number(label="Amount to Deposit")
                withdraw_amount_input = gr.Number(label="Amount to Withdraw")
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            deposit_status_output = gr.Textbox(label="Deposit Status", interactive=False)
            withdraw_status_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        with gr.TabItem("Buy/Sell Shares"):
            with gr.Row():
                share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
                share_quantity_input = gr.Number(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            buy_sell_status_output = gr.Textbox(label="Buy/Sell Status", interactive=False)

        with gr.TabItem("Account Summary & Transactions"):
            view_summary_btn = gr.Button("Refresh Account Summary")
            transactions_display = gr.DataFrame(
                headers=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Amount", "Description"],
                datatype=["str", "str", "str", "str", "str", "str", "str"],
                interactive=False,
                label="Transaction History"
            )

    # --- Event Listeners ---
    create_account_btn.click(
        fn=create_or_get_account,
        inputs=[account_id_input],
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    deposit_btn.click(
        fn=deposit_wrapper,
        inputs=[deposit_amount_input],
        outputs=[deposit_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    withdraw_btn.click(
        fn=withdraw_wrapper,
        inputs=[withdraw_amount_input],
        outputs=[withdraw_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    buy_btn.click(
        fn=buy_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    sell_btn.click(
        fn=sell_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    view_summary_btn.click(
        fn=update_account_displays,
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )
    
    # Auto-update displays after each transaction for better UX
    deposit_btn.click(fn=update_account_displays, outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    withdraw_btn.click(fn=update_account_displays, outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    buy_btn.click(fn=update_account_displays, outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])
    sell_btn.click(fn=update_account_displays, outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display])

demo.launch()
```

The `process_transaction` helper was making things too complex and potentially overriding status messages. It's better to handle the update of all display components after each transaction directly in the `click` events, or by having a central `update_account_displays` function that is called.

Let's simplify the structure and ensure all outputs are correctly linked.
The `update_account_displays` function seems the most robust way to refresh all the main display components.

Final check on the requirements and outputs:
- Create account: Yes
- Deposit/Withdraw: Yes
- Buy/Sell Shares: Yes
- Portfolio Value: Yes
- Profit/Loss: Yes
- Holdings: Yes
- Transactions: Yes
- Error Handling (negative balance, insufficient shares/funds): Yes, relies on `Account` class.

The structure with `gr.Blocks` and specific event handlers for each button, updating multiple outputs including the summary displays, looks correct. I need to make sure the `update_account_displays` function is called appropriately. It seems I had it called twice on `click` events; that should be reduced to once.

The `update_account_displays` function needs to return ALL the outputs that need to be updated after a transaction.
The `deposit_btn.click`, `withdraw_btn.click`, etc., should call the wrapper functions (which do the transaction and return a status message), and THEN call `update_account_displays` to refresh the rest. This is tricky with Gradio's single-function-per-event-handler model.

A better pattern:
1. Button click calls transaction wrapper (`deposit_wrapper`).
2. Transaction wrapper performs the action and returns status + updated account state.
3. These outputs are mapped to respective UI components.
This is what I have attempted in the last draft.

Let's refine `update_account_displays` and how it's called. The `transaction_wrapper` approach might be the cleaner way if it returns all the necessary values.

Rethinking `process_transaction`:
It should take the transaction function and its arguments, call it, get its status, and then call `update_account_displays` to get the latest state for all summary fields and the transaction table.
The problem is how to return multiple status messages (one for deposit, one for buy/sell) and then also the full account summary.

Let's consider the output mapping for a `deposit_btn.click`:
`inputs=[deposit_amount_input]`
`outputs=[deposit_status_output, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]`
The `deposit_wrapper` function needs to return these 7 values.

`deposit_wrapper(amount_input)`:
1. Call `account.deposit(amount)`.
2. Get status message.
3. Call `update_account_displays()` to get all the account state.
4. Return `[status_msg, *update_account_displays()[1:]]`. This way, `deposit_status_output` gets `status_msg`, and the rest of the outputs get the data from `update_account_displays`.

This pattern seems correct.
The `update_account_displays` function should ONLY return the 7 values that represent the account state. The status messages for each tab should be handled separately by the specific transaction wrappers.

So, the `deposit_wrapper` would look like:
```python
def deposit_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *update_account_displays()[1:] # Return error and current state
    try:
        amount = float(amount_input)
        if account.deposit(amount):
            status_msg = f"Deposit successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Deposit failed. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered."

    # Now get the latest account state to refresh all displays
    _, acc_id, bal, hold, port_val, total_val, pnl, txns = update_account_displays()
    return status_msg, acc_id, bal, hold, port_val, total_val, pnl, txns
```
This seems like the right approach. I need to apply this pattern to all transaction wrappers.

Let's re-verify the outputs of `update_account_displays`:
`return (f"Account ID: {account.account_id}", account.account_id, balance, holdings_str, portfolio_value, total_value, f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})", format_transactions_for_display(account.get_transactions()))`
This returns 8 items. The transaction wrappers need to return 7 items (status + 6 summary fields + transactions). This is a mismatch.

The `update_account_displays` should just return the *account state* fields, not the status line.
Let's redefine `update_account_displays` to return only the state:
`return acc_id, balance, holdings_str, portfolio_value, total_value, pnl_str, formatted_txns` (7 items)

Then, each wrapper will return `status_msg, *update_account_displays()`.

```python
import gradio as gr
import accounts # Assuming accounts.py is in the same directory

# Global variable to hold the single account instance for this demo
account = None

def format_transactions_for_display(transactions):
    """Formats a list of Transaction objects into a list of lists for gr.DataFrame."""
    if not transactions:
        return []
    
    formatted_data = []
    for tx in transactions:
        formatted_data.append([
            tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            tx.transaction_type,
            tx.symbol if tx.symbol else "",
            tx.quantity if tx.quantity is not None else "",
            f"{tx.price:.2f}" if tx.price is not None else "",
            f"{tx.amount:.2f}",
            tx.description
        ])
    return formatted_data

def get_current_account_state():
    """Helper function to return all current account state for display components."""
    if account is None:
        return "", 0.0, "No holdings", 0.0, 0.0, "N/A", [] # 7 items
    
    holdings_dict = account.get_holdings()
    holdings_str = "\n".join([f"{symbol}: {qty}" for symbol, qty in holdings_dict.items()]) if holdings_dict else "No holdings"
    
    balance = account.get_balance()
    portfolio_value = account.get_portfolio_value()
    total_value = account.get_total_account_value()
    profit_loss = account.get_profit_loss()
    initial_deposit = account.get_initial_deposit()
    
    pnl_str = f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})"

    return (account.account_id,
            balance,
            holdings_str,
            portfolio_value,
            total_value,
            pnl_str,
            format_transactions_for_display(account.get_transactions())) # 7 items

def create_or_get_account(account_id_input):
    global account
    if not account_id_input:
        return "Error: Account ID cannot be empty.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
        
    if account is None:
        try:
            account = accounts.Account(account_id_input)
            status_msg = f"Account '{account_id_input}' created successfully."
            # Return status message + the current account state
            return status_msg, *get_current_account_state()
        except ValueError as e:
            return f"Error creating account: {e}", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
    else:
        if account.account_id == account_id_input:
            status_msg = f"Account '{account_id_input}' already active."
            return status_msg, *get_current_account_state()
        else:
            return f"Error: Another account ('{account.account_id}') is already active. Please restart the demo to switch accounts.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []

# --- Transaction Wrappers ---
def deposit_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.deposit(amount):
            status_msg = f"Deposit successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Deposit failed. Check logs." # Account class prints errors
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for deposit."

    return status_msg, *get_current_account_state() # Return status + updated account state

def withdraw_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.withdraw(amount):
            status_msg = f"Withdrawal successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Withdrawal failed. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for withdrawal."

    return status_msg, *get_current_account_state()

def buy_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.buy_shares(symbol_input, quantity):
            status_msg = f"Buy order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Buy order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for buying shares."

    return status_msg, *get_current_account_state()

def sell_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.sell_shares(symbol_input, quantity):
            status_msg = f"Sell order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Sell order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for selling shares."

    return status_msg, *get_current_account_state()


with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulation")

    # --- Account Management Section ---
    with gr.Row():
        account_id_input = gr.Textbox(label="Account ID", placeholder="Enter your desired Account ID")
        create_account_btn = gr.Button("Create/Activate Account")

    # Output fields for account status and summary
    account_status_output = gr.Textbox(label="Account Status", interactive=False)
    active_account_id_display = gr.Textbox(label="Active Account ID", interactive=False)
    current_balance_display = gr.Number(label="Current Balance", interactive=False)
    holdings_display = gr.Textbox(label="Current Holdings", interactive=False, lines=3)
    portfolio_value_display = gr.Number(label="Portfolio Value", interactive=False)
    total_account_value_display = gr.Number(label="Total Account Value", interactive=False)
    profit_loss_display = gr.Textbox(label="Profit/Loss (vs Initial Deposit)", interactive=False)

    # --- Transaction Section ---
    with gr.Tabs():
        with gr.TabItem("Deposit/Withdraw"):
            with gr.Row():
                deposit_amount_input = gr.Number(label="Amount to Deposit", precision=2)
                withdraw_amount_input = gr.Number(label="Amount to Withdraw", precision=2)
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            deposit_status_output = gr.Textbox(label="Deposit Status", interactive=False)
            withdraw_status_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        with gr.TabItem("Buy/Sell Shares"):
            with gr.Row():
                share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
                share_quantity_input = gr.Number(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            buy_sell_status_output = gr.Textbox(label="Buy/Sell Status", interactive=False)

        with gr.TabItem("Account Summary & Transactions"):
            view_summary_btn = gr.Button("Refresh Account Summary")
            transactions_display = gr.DataFrame(
                headers=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Amount", "Description"],
                datatype=["str", "str", "str", "str", "str", "str", "str"],
                interactive=False,
                label="Transaction History"
            )

    # --- Event Listeners ---
    # Account Creation
    create_account_btn.click(
        fn=create_or_get_account,
        inputs=[account_id_input],
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Deposit Transaction
    deposit_btn.click(
        fn=deposit_wrapper,
        inputs=[deposit_amount_input],
        outputs=[deposit_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Withdraw Transaction
    withdraw_btn.click(
        fn=withdraw_wrapper,
        inputs=[withdraw_amount_input],
        outputs=[withdraw_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Buy Shares Transaction
    buy_btn.click(
        fn=buy_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Sell Shares Transaction
    sell_btn.click(
        fn=sell_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Manual Refresh of Account Summary
    view_summary_btn.click(
        fn=get_current_account_state, # Just get the state, not a status message
        outputs=[active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )
    
    # Note: The status outputs for each tab (deposit_status_output, etc.)
    # are updated directly by their respective wrapper functions.
    # The get_current_account_state is for explicitly refreshing the summary section.

demo.launch()
```
The `account_status_output` is only used for the initial account creation message or error. It's not intended to be continuously updated after transactions. The status for each transaction tab is handled by `deposit_status_output`, etc. The `active_account_id_display` is part of the general account state.

One final check on `create_or_get_account` output mapping. It needs to fill all summary fields and the transaction table.

`create_or_get_account` outputs:
`[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]`
This is 8 outputs.
`get_current_account_state` returns 7 items.
The `account_status_output` is extra in `create_or_get_account`. This is correct.

All transaction wrappers should return 8 items: `[status_msg, *get_current_account_state()]`.
The `create_account_btn.click` also needs to return these 8 items.

Let's ensure all `outputs` lists match the number of return values from the functions.
`create_or_get_account` returns 8. Outputs list has 8. Correct.
`deposit_wrapper` returns 8. Outputs list has 8. Correct.
Same for others.
The `view_summary_btn.click` returns 7 outputs from `get_current_account_state`. This is correct because it doesn't need to update the `account_status_output` which is for the initial status.

The code looks good.
```python
import gradio as gr
import accounts

# Global variable to hold the single account instance for this demo
account = None

def format_transactions_for_display(transactions):
    """Formats a list of Transaction objects into a list of lists for gr.DataFrame."""
    if not transactions:
        return []
    
    formatted_data = []
    for tx in transactions:
        formatted_data.append([
            tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            tx.transaction_type,
            tx.symbol if tx.symbol else "",
            tx.quantity if tx.quantity is not None else "",
            f"{tx.price:.2f}" if tx.price is not None else "",
            f"{tx.amount:.2f}",
            tx.description
        ])
    return formatted_data

def get_current_account_state():
    """Helper function to return all current account state for display components."""
    if account is None:
        # Return default empty states for all summary fields
        return "", 0.0, "No holdings", 0.0, 0.0, "N/A", [] # 7 items
    
    holdings_dict = account.get_holdings()
    holdings_str = "\n".join([f"{symbol}: {qty}" for symbol, qty in holdings_dict.items()]) if holdings_dict else "No holdings"
    
    balance = account.get_balance()
    portfolio_value = account.get_portfolio_value()
    total_value = account.get_total_account_value()
    profit_loss = account.get_profit_loss()
    initial_deposit = account.get_initial_deposit()
    
    pnl_str = f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})"

    return (account.account_id,
            balance,
            holdings_str,
            portfolio_value,
            total_value,
            pnl_str,
            format_transactions_for_display(account.get_transactions())) # 7 items

def create_or_get_account(account_id_input):
    global account
    if not account_id_input:
        # Return an error status and default empty account state
        return "Error: Account ID cannot be empty.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
        
    if account is None:
        try:
            account = accounts.Account(account_id_input)
            status_msg = f"Account '{account_id_input}' created successfully."
            # Return status message and the newly created account's state
            return status_msg, *get_current_account_state()
        except ValueError as e:
            # Return error message and default empty account state
            return f"Error creating account: {e}", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
    else:
        if account.account_id == account_id_input:
            status_msg = f"Account '{account_id_input}' already active."
            # Return status message and the current account's state
            return status_msg, *get_current_account_state()
        else:
            # Return error if a different account is already active
            return f"Error: Another account ('{account.account_id}') is already active. Please restart the demo to switch accounts.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []

# --- Transaction Wrappers ---
# These functions perform a transaction, return a status message for their tab,
# and then refresh all the main account summary displays.

def deposit_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.deposit(amount):
            status_msg = f"Deposit successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Deposit failed. Check logs." # Account class prints specific errors
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for deposit."

    # Return status message for the deposit tab, and updated state for all summary fields
    return status_msg, *get_current_account_state()

def withdraw_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.withdraw(amount):
            status_msg = f"Withdrawal successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Withdrawal failed. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for withdrawal."

    return status_msg, *get_current_account_state()

def buy_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.buy_shares(symbol_input, quantity):
            status_msg = f"Buy order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Buy order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for buying shares."

    return status_msg, *get_current_account_state()

def sell_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.sell_shares(symbol_input, quantity):
            status_msg = f"Sell order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Sell order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for selling shares."

    return status_msg, *get_current_account_state()


with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulation")

    # --- Account Management Section ---
    with gr.Row():
        account_id_input = gr.Textbox(label="Account ID", placeholder="Enter your desired Account ID")
        create_account_btn = gr.Button("Create/Activate Account")

    # Output fields for account status and summary
    account_status_output = gr.Textbox(label="Account Status", interactive=False)
    active_account_id_display = gr.Textbox(label="Active Account ID", interactive=False)
    current_balance_display = gr.Number(label="Current Balance", interactive=False)
    holdings_display = gr.Textbox(label="Current Holdings", interactive=False, lines=3)
    portfolio_value_display = gr.Number(label="Portfolio Value", interactive=False)
    total_account_value_display = gr.Number(label="Total Account Value", interactive=False)
    profit_loss_display = gr.Textbox(label="Profit/Loss (vs Initial Deposit)", interactive=False)

    # --- Transaction Section ---
    with gr.Tabs():
        with gr.TabItem("Deposit/Withdraw"):
            with gr.Row():
                deposit_amount_input = gr.Number(label="Amount to Deposit", precision=2)
                withdraw_amount_input = gr.Number(label="Amount to Withdraw", precision=2)
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            deposit_status_output = gr.Textbox(label="Deposit Status", interactive=False)
            withdraw_status_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        with gr.TabItem("Buy/Sell Shares"):
            with gr.Row():
                share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
                share_quantity_input = gr.Number(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            buy_sell_status_output = gr.Textbox(label="Buy/Sell Status", interactive=False)

        with gr.TabItem("Account Summary & Transactions"):
            view_summary_btn = gr.Button("Refresh Account Summary")
            transactions_display = gr.DataFrame(
                headers=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Amount", "Description"],
                datatype=["str", "str", "str", "str", "str", "str", "str"],
                interactive=False,
                label="Transaction History"
            )

    # --- Event Listeners ---
    # Account Creation: Updates status and all summary fields
    create_account_btn.click(
        fn=create_or_get_account,
        inputs=[account_id_input],
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Deposit Transaction: Updates deposit status and all summary fields
    deposit_btn.click(
        fn=deposit_wrapper,
        inputs=[deposit_amount_input],
        outputs=[deposit_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Withdraw Transaction: Updates withdrawal status and all summary fields
    withdraw_btn.click(
        fn=withdraw_wrapper,
        inputs=[withdraw_amount_input],
        outputs=[withdraw_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Buy Shares Transaction: Updates buy/sell status and all summary fields
    buy_btn.click(
        fn=buy_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Sell Shares Transaction: Updates buy/sell status and all summary fields
    sell_btn.click(
        fn=sell_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Manual Refresh of Account Summary: Updates all summary fields (but not the tab-specific status messages)
    view_summary_btn.click(
        fn=get_current_account_state,
        outputs=[active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )
    
    demo.launch()
``````python
import gradio as gr
import accounts

# Global variable to hold the single account instance for this demo
account = None

def format_transactions_for_display(transactions):
    """Formats a list of Transaction objects into a list of lists for gr.DataFrame."""
    if not transactions:
        return []
    
    formatted_data = []
    for tx in transactions:
        formatted_data.append([
            tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            tx.transaction_type,
            tx.symbol if tx.symbol else "",
            tx.quantity if tx.quantity is not None else "",
            f"{tx.price:.2f}" if tx.price is not None else "",
            f"{tx.amount:.2f}",
            tx.description
        ])
    return formatted_data

def get_current_account_state():
    """Helper function to return all current account state for display components."""
    if account is None:
        # Return default empty states for all summary fields
        return "", 0.0, "No holdings", 0.0, 0.0, "N/A", [] # 7 items
    
    holdings_dict = account.get_holdings()
    holdings_str = "\n".join([f"{symbol}: {qty}" for symbol, qty in holdings_dict.items()]) if holdings_dict else "No holdings"
    
    balance = account.get_balance()
    portfolio_value = account.get_portfolio_value()
    total_value = account.get_total_account_value()
    profit_loss = account.get_profit_loss()
    initial_deposit = account.get_initial_deposit()
    
    pnl_str = f"${profit_loss:.2f} (Initial Deposit: ${initial_deposit:.2f})"

    return (account.account_id,
            balance,
            holdings_str,
            portfolio_value,
            total_value,
            pnl_str,
            format_transactions_for_display(account.get_transactions())) # 7 items

def create_or_get_account(account_id_input):
    global account
    if not account_id_input:
        # Return an error status and default empty account state
        return "Error: Account ID cannot be empty.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
        
    if account is None:
        try:
            account = accounts.Account(account_id_input)
            status_msg = f"Account '{account_id_input}' created successfully."
            # Return status message and the newly created account's state
            return status_msg, *get_current_account_state()
        except ValueError as e:
            # Return error message and default empty account state
            return f"Error creating account: {e}", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []
    else:
        if account.account_id == account_id_input:
            status_msg = f"Account '{account_id_input}' already active."
            # Return status message and the current account's state
            return status_msg, *get_current_account_state()
        else:
            # Return error if a different account is already active
            return f"Error: Another account ('{account.account_id}') is already active. Please restart the demo to switch accounts.", "", 0.0, "No holdings", 0.0, 0.0, "N/A", []

# --- Transaction Wrappers ---
# These functions perform a transaction, return a status message for their tab,
# and then refresh all the main account summary displays.

def deposit_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.deposit(amount):
            status_msg = f"Deposit successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Deposit failed. Check logs." # Account class prints specific errors
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for deposit."

    # Return status message for the deposit tab, and updated state for all summary fields
    return status_msg, *get_current_account_state()

def withdraw_wrapper(amount_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    try:
        amount = float(amount_input)
        if account.withdraw(amount):
            status_msg = f"Withdrawal successful. Amount: ${amount:.2f}"
        else:
            status_msg = "Withdrawal failed. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid amount entered for withdrawal."

    return status_msg, *get_current_account_state()

def buy_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.buy_shares(symbol_input, quantity):
            status_msg = f"Buy order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Buy order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for buying shares."

    return status_msg, *get_current_account_state()

def sell_shares_wrapper(symbol_input, quantity_input):
    if account is None:
        return "Error: No account active.", *get_current_account_state()
    if not symbol_input:
        return "Error: Symbol cannot be empty.", *get_current_account_state()
    try:
        quantity = int(quantity_input)
        if account.sell_shares(symbol_input, quantity):
            status_msg = f"Sell order successful: {quantity} shares of {symbol_input}."
        else:
            status_msg = f"Sell order failed for {symbol_input}. Check logs."
    except (ValueError, TypeError):
        status_msg = "Error: Invalid quantity entered for selling shares."

    return status_msg, *get_current_account_state()


with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Simulation")

    # --- Account Management Section ---
    with gr.Row():
        account_id_input = gr.Textbox(label="Account ID", placeholder="Enter your desired Account ID")
        create_account_btn = gr.Button("Create/Activate Account")

    # Output fields for account status and summary
    account_status_output = gr.Textbox(label="Account Status", interactive=False)
    active_account_id_display = gr.Textbox(label="Active Account ID", interactive=False)
    current_balance_display = gr.Number(label="Current Balance", interactive=False)
    holdings_display = gr.Textbox(label="Current Holdings", interactive=False, lines=3)
    portfolio_value_display = gr.Number(label="Portfolio Value", interactive=False)
    total_account_value_display = gr.Number(label="Total Account Value", interactive=False)
    profit_loss_display = gr.Textbox(label="Profit/Loss (vs Initial Deposit)", interactive=False)

    # --- Transaction Section ---
    with gr.Tabs():
        with gr.TabItem("Deposit/Withdraw"):
            with gr.Row():
                deposit_amount_input = gr.Number(label="Amount to Deposit", precision=2)
                withdraw_amount_input = gr.Number(label="Amount to Withdraw", precision=2)
            with gr.Row():
                deposit_btn = gr.Button("Deposit")
                withdraw_btn = gr.Button("Withdraw")
            deposit_status_output = gr.Textbox(label="Deposit Status", interactive=False)
            withdraw_status_output = gr.Textbox(label="Withdrawal Status", interactive=False)

        with gr.TabItem("Buy/Sell Shares"):
            with gr.Row():
                share_symbol_input = gr.Textbox(label="Share Symbol (e.g., AAPL, TSLA, GOOGL)")
                share_quantity_input = gr.Number(label="Quantity")
            with gr.Row():
                buy_btn = gr.Button("Buy Shares")
                sell_btn = gr.Button("Sell Shares")
            buy_sell_status_output = gr.Textbox(label="Buy/Sell Status", interactive=False)

        with gr.TabItem("Account Summary & Transactions"):
            view_summary_btn = gr.Button("Refresh Account Summary")
            transactions_display = gr.DataFrame(
                headers=["Timestamp", "Type", "Symbol", "Quantity", "Price", "Amount", "Description"],
                datatype=["str", "str", "str", "str", "str", "str", "str"],
                interactive=False,
                label="Transaction History"
            )

    # --- Event Listeners ---
    # Account Creation: Updates status and all summary fields
    create_account_btn.click(
        fn=create_or_get_account,
        inputs=[account_id_input],
        outputs=[account_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Deposit Transaction: Updates deposit status and all summary fields
    deposit_btn.click(
        fn=deposit_wrapper,
        inputs=[deposit_amount_input],
        outputs=[deposit_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Withdraw Transaction: Updates withdrawal status and all summary fields
    withdraw_btn.click(
        fn=withdraw_wrapper,
        inputs=[withdraw_amount_input],
        outputs=[withdraw_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Buy Shares Transaction: Updates buy/sell status and all summary fields
    buy_btn.click(
        fn=buy_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Sell Shares Transaction: Updates buy/sell status and all summary fields
    sell_btn.click(
        fn=sell_shares_wrapper,
        inputs=[share_symbol_input, share_quantity_input],
        outputs=[buy_sell_status_output, active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )

    # Manual Refresh of Account Summary: Updates all summary fields (but not the tab-specific status messages)
    view_summary_btn.click(
        fn=get_current_account_state,
        outputs=[active_account_id_display, current_balance_display, holdings_display, portfolio_value_display, total_account_value_display, profit_loss_display, transactions_display]
    )
    
    demo.launch()
```