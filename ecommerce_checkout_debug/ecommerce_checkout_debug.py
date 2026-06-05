import logging
import pdb

# ----------------------------
# LOGGING CONFIGURATION
# ----------------------------
logging.basicConfig(
    filename="checkout.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# SAMPLE CART
# ----------------------------
cart = [
    {"name": "Laptop", "price": 1000},
    {"name": "Mouse", "price": 50},
    {"name": "Keyboard", "price": 100}
]

# ----------------------------
# CALCULATE TOTAL
# ----------------------------
def calculate_total(cart_items):
    total = 0

    for item in cart_items:
        price = item.get("price", 0)
        total += price

    logging.info(f"Cart total calculated: {total}")
    return total


# ----------------------------
# APPLY DISCOUNT (BUG INTRODUCED HERE)
# ----------------------------
def apply_discount(total, discount_percent):

    pdb.set_trace()  # <-- Debugger breakpoint

    # INTENTIONAL BUG: Wrong formula (missing /100)
    discount_amount = total * discount_percent

    logging.info(f"Discount calculated (BUGGED): {discount_amount}")

    final_total = total - discount_amount
    return final_total


# ----------------------------
# CHECKOUT PROCESS
# ----------------------------
def checkout(cart_items, discount_percent):
    try:
        if not cart_items:
            raise ValueError("Cart is empty")

        total = calculate_total(cart_items)
        logging.info(f"Total before discount: {total}")

        final_total = apply_discount(total, discount_percent)

        logging.info(f"Final total after discount: {final_total}")

        print("----- CHECKOUT SUMMARY -----")
        print(f"Total: {total}")
        print(f"Discount: {discount_percent}%")
        print(f"Final Total: {final_total}")

    except Exception as error:
        logging.error(f"Checkout error: {error}")
        print("An error occurred during checkout:", error)


# ----------------------------
# RUN PROGRAM
# ----------------------------
if __name__ == "__main__":
    checkout(cart, discount_percent=10)