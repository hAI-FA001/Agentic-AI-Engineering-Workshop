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