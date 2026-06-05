# E-Commerce Checkout Debugging System

## Overview

This Python program simulates a simple e-commerce checkout process while demonstrating debugging and logging techniques.

The program:

* Calculates the total cost of items in a shopping cart
* Applies a percentage discount to the cart total
* Intentionally introduces a bug in the discount calculation
* Uses Python's built-in `pdb` debugger to inspect program execution
* Logs cart totals, discounts, and errors to a log file
* Handles checkout-related exceptions gracefully

## Features

* Shopping cart simulation
* Cart total calculation
* Discount application
* Intentional bug for debugging practice
* Interactive debugging with `pdb`
* Transaction and error logging
* Exception handling
* Clear checkout summary output

## Technologies Used

* Python 3

## Required Libraries

No external libraries are required.

This program uses only Python built-in libraries:

* logging
* pdb

## How to Run the Program

### 1. Navigate into the folder

cd ecommerce_checkout_debug

### 2. Run the program

python ecommerce_checkout_debug.py

## Debugging the Program

When the program reaches the discount calculation function, execution will pause at the debugger breakpoint:

pdb.set_trace()

Useful debugger commands:

* `n` — Execute the next line
* `s` — Step into a function
* `p variable_name` — Print a variable value
* `c` — Continue execution
* `q` — Quit the debugger

## Log File

The program automatically creates a log file:

checkout.log

The log file records:

* Cart totals
* Discount calculations
* Final checkout totals
* Checkout errors
