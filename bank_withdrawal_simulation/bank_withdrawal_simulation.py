# Import Decimal for accurate money calculations
# Import InvalidOperation to catch invalid numeric inputs
from decimal import Decimal, InvalidOperation

# Import datetime for transaction logging timestamps
from datetime import datetime


# Custom exception for insufficient account balance
class InsufficientFundsError(Exception):
    """Raised when withdrawal exceeds account balance."""
    pass


class BankAccount:

    # Constructor to initialize account balance
    def __init__(self, balance=0):
        """
        Create a new bank account.

        Args:
            balance:
                Starting account balance.
                Accepts int, float, str, or Decimal.
        """

        # Validate the starting balance before storing it
        self.balance = self._validate_amount(balance, allow_zero=True)

    # Static method because it does not depend on instance variables
    @staticmethod
    def _validate_amount(amount, allow_zero=False):
        """
        Validate and sanitize monetary input.

        Args:
            amount:
                The amount to validate.

            allow_zero:
                If True, zero is allowed.
                If False, amount must be greater than zero.

        Returns:
            Decimal:
                Cleaned and validated amount.
        """

        try:
            # Convert amount safely to Decimal
            # str() prevents float precision issues
            amount = Decimal(str(amount))

        except (InvalidOperation, ValueError):

            # Raised if conversion fails
            raise TypeError("Amount must be a valid number.")

        # Prevent invalid Decimal values
        if amount.is_nan() or amount.is_infinite():
            raise ValueError("Amount cannot be NaN or infinite.")

        # Validation when zero is allowed
        if allow_zero:

            # Negative amounts are not allowed
            if amount < 0:
                raise ValueError("Amount cannot be negative.")

        # Validation when zero is NOT allowed
        else:

            # Amount must be greater than zero
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

        # Round to 2 decimal places
        # Standard practice for currency systems
        return amount.quantize(Decimal("0.01"))

    # Deposit money into account
    def deposit(self, amount):
        """
        Deposit money into the account.
        """

        # Validate deposit amount
        amount = self._validate_amount(amount)

        # Add deposit amount to balance
        self.balance += amount

        # Return success message
        return (
            f"Deposit successful. "
            f"New balance: ₦{self.balance}"
        )

    # Withdraw money from account
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        """

        # Validate withdrawal amount
        amount = self._validate_amount(amount)

        # Check if withdrawal exceeds balance
        if amount > self.balance:

            # Raise custom exception
            raise InsufficientFundsError(
                f"Insufficient funds. "
                f"Available balance: ₦{self.balance}"
            )

        # Subtract amount from balance
        self.balance -= amount

        # Return success message
        return (
            f"Withdrawal successful. "
            f"Remaining balance: ₦{self.balance}"
        )


# Function to simulate transaction logging
def log_transaction(status, amount, message):
    """
    Log transaction details.
    """

    # Get current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Print formatted transaction log
    print(
        f"[{timestamp}] "
        f"STATUS: {status} | "
        f"AMOUNT: ₦{amount} | "
        f"MESSAGE: {message}"
    )


# Main program execution
def main():

    # Create bank account with initial balance
    account = BankAccount(balance=50000)

    # Display current balance
    print(f"Current Balance: ₦{account.balance}")

    # Default transaction amount
    amount = Decimal("0.00")

    # Track transaction success properly
    transaction_successful = False

    result_message = "No transaction executed."

    try:

        # Collect user input
        user_input = input("Enter withdrawal amount: ").strip()

        # Prevent empty input
        if not user_input:
            raise ValueError("Input cannot be empty.")

        # Convert input to Decimal
        amount = Decimal(user_input)

        # Attempt withdrawal
        result_message = account.withdraw(amount)

    # Handle invalid inputs
    except (ValueError, TypeError, InvalidOperation) as error:

        print(f"Input Error: {error}")

    # Handle insufficient balance
    except InsufficientFundsError as error:

        print(f"Transaction Failed: {error}")

    # Runs only if NO exception occurs
    else:

        # Mark transaction as successful
        transaction_successful = True

        # Print successful transaction message
        print(result_message)

    # Always runs whether exception occurs or not
    finally:

        # Determine accurate transaction status
        status = (
            "COMPLETED" if transaction_successful else "FAILED")

        # Log transaction details
        log_transaction(
            status=status,

            # Prevent None from printing
            amount=amount,

            message=result_message
        )


# Entry point of the program
# Ensures file runs directly, not when imported
if __name__ == "__main__":
    main()