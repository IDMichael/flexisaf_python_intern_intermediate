# ==========================
# Employee Base Class
# ==========================
class Employee:

    # Initialize an employee with a name and salary.
    def __init__(self, name, salary):

        # Validate that the name is a non-empty string.
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Employee name cannot be empty.")

        # Validate that the salary is not negative.
        if salary < 0:
            raise ValueError("Salary cannot be negative.")

        self.name = name
        self.salary = salary

    # Must be implemented by subclasses.
    def calculate_bonus(self):
        raise NotImplementedError(
            "Subclasses must implement calculate_bonus()"
        )

    # Return salary plus bonus.
    def total_pay(self):
        return self.salary + self.calculate_bonus()


# ==========================
# Employee Types
# ==========================

# Manager receives a 30% bonus.
class Manager(Employee):

    def calculate_bonus(self):
        return self.salary * 0.30


# Developer receives a 20% bonus.
class Developer(Employee):

    def calculate_bonus(self):
        return self.salary * 0.20


# ==========================
# Payment Base Class
# ==========================

class Payment:

    # Must be implemented by payment subclasses.
    def process_payment(self, employee, amount):
        raise NotImplementedError(
            "Subclasses must implement process_payment()."
        )


# ==========================
# Credit Card Payment
# ==========================

class CreditCardPayment(Payment):

    # Store the credit card number.
    def __init__(self, card_number):

        # Validate card number.
        if len(card_number) < 4:
            raise ValueError("Invalid card number.")

        self.card_number = card_number

    # Simulate payment using a credit card.
    def process_payment(self, employee, amount):
        print(
            f"Paying {employee.name} "
            f"N{amount:,.2f} "
            f"via Credit Card ending in "
            f"{self.card_number[-4:]}"
        )


# ==========================
# PayPal Payment
# ==========================

class PayPalPayment(Payment):

    # Store the PayPal email.
    def __init__(self, email):

        # Validate email.
        if "@" not in email:
            raise ValueError("Invalid Paypal Email.")

        self.email = email

    # Simulate payment using PayPal.
    def process_payment(self, employee, amount):
        print(
            f"Paying {employee.name} "
            f"N{amount:,.2f} "
            f"via Paypal Account "
            f"{self.email}"
        )


# ==========================
# Bank Transfer Payment
# ==========================

class BankTransferPayment(Payment):

    # Store the account number.
    def __init__(self, account_number):

        # Validate account number.
        if not account_number.strip():
            raise ValueError("Account number cannot be empty.")

        self.account_number = account_number

    # Simulate payment using bank transfer.
    def process_payment(self, employee, amount):
        print(
            f"Paying {employee.name} "
            f"N{amount:,.2f} "
            f"via Bank Transfer to account "
            f"{self.account_number}"
        )


# ==========================
# Payroll System
# ==========================

class PayrollSystem:

    # Create an empty employee list.
    def __init__(self):
        self.employees = []

    # Register an employee and assign a payment method.
    def add_employee(self, employee, payment_method):

        # Ensure employee is an Employee object.
        if not isinstance(employee, Employee):
            raise TypeError("Must be an Employee object.")

        # Ensure payment method is a Payment object.
        if not isinstance(payment_method, Payment):
            raise TypeError("Must be a Payment object.")

        # Associate a payment method with the employee.
        employee.payment_method = payment_method

        # Add employee to payroll.
        self.employees.append(employee)

    # Process payroll for every employee.
    def process_payroll(self):

        print("\n==== PAYROLL REPORT ====")

        # Process employees one at a time.
        for employee in self.employees:

            # Calculate employee bonus.
            bonus = employee.calculate_bonus()

            # Calculate total payment.
            total_amount = employee.total_pay()

            # Display payroll information.
            print(f"Employee: {employee.name}")
            print(f"Base Salary: N{employee.salary:,.2f}")
            print(f"Bonus: N{bonus:,.2f}")
            print(f"Total Pay: N{total_amount:,.2f}")

            # Process payment using the employee's payment method.
            employee.payment_method.process_payment(
                employee,
                total_amount
            )

            print("-" * 64)


# ==========================
# Demonstration
# ==========================

# Create employees.
manager1 = Manager("Michael", 60000)
manager2 = Manager("Imami", 50000)

developer1 = Developer("Mark", 2000)
developer2 = Developer("Matthew", 3000)

# Create payment methods.
credit_card = CreditCardPayment("19018234561782901")
paypal = PayPalPayment("mild@gmail.com")
bank_transfer = BankTransferPayment("2134566789")

# Create payroll system.
payroll = PayrollSystem()

# Register employees with their payment methods.
payroll.add_employee(manager1, credit_card)
payroll.add_employee(manager2, bank_transfer)

payroll.add_employee(developer1, paypal)
payroll.add_employee(developer2, credit_card)

# Run payroll.
payroll.process_payroll()